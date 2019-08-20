from flask import Flask, jsonify, url_for
app = Flask(__name__)
app.config.update(
    # CELERY_BROKER_URL='amqp://myuser:mypassword@127.0.0.1:8004/myvhost',
    # CELERY_RESULT_BACKEND='amqp://myuser:mypassword@127.0.0.1:8004/myvhost'
    CELERY_BROKER_URL='amqp://guest:guest@127.0.0.1:5672',
    CELERY_RESULT_BACKEND='amqp://guest:guest@127.0.0.1:5672'
)
print('__file__={0:<35} | __name__={1:<20} | __package__={2:<20}'.format(__file__,__name__,str(__package__)))
import services
import services.read_file
from services.read_file import getDataFromTestFile

# import services.celery
from services.celery import make_celery

import json

celery = make_celery(app)

@celery.task(bind=True)
def process_full_data_task(self):
    response = getDataFromTestFile("datafile.txt")
    resDic = json.loads(response)
    country = resDic["country_with_max_count"]
    return {'status': 'Task completed!!','current': 100, 'total': 100, 'result': 100, 'country_with_max_count': country}

@app.route("/")
def hello():
    return "Hello World from Flask!!!"

@app.route('/get-partial-data', methods=['GET'])
def get_partial_data():
    return getDataFromTestFile("datafile_partial.txt")

@app.route('/process-full-data', methods=['GET'])
def process_full_data():
    task = process_full_data_task.apply_async()
    return jsonify({'location': url_for('taskstatus',task_id=task.id)}), 202, {'Location': url_for('taskstatus',task_id=task.id)}

@app.route('/status/<task_id>')
def taskstatus(task_id):
    task = process_full_data_task.AsyncResult(task_id)
    if task.state == 'PENDING':
        # job did not start yet
        response = {
            'state': task.state,
            'current': 0,
            'total': 1,
            'status': 'Pending...'
        }
    elif task.state != 'FAILURE':
        response = {
            'state': task.state,
            'current': task.info.get('current', 0),
            'total': task.info.get('total', 1),
            'status': task.info.get('status', '')
        }
        if 'result' in task.info:
            response['result'] = task.info['result']
    else:
        # something went wrong in the background job
        response = {
            'state': task.state,
            'current': 1,
            'total': 1,
            'status': str(task.info),  # this is the exception raised
        }
    return jsonify(response)

if __name__ == "__main__":
    # Only for debugging while developing
    app.run(host='0.0.0.0', debug=True, port=80)
