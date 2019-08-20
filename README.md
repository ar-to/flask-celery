# Pigeonly Programming Test

## Quick Start

Via Docker Compose
```shell
docker-compose up
# http://127.0.0.1:5001
# see endpoints below
# http://127.0.0.1:5001/get-partial-data - GET request to process a shorter datafile_test.txt
# http://127.0.0.1:5001/process-full-data - GET request to run celery task and process the full datafile.txt async; returns the /statu/task_id
# http://127.0.0.1:5001/status/0d3fdac5-242a-4d5b-8af7-91f90456647d - GET request used to track process
```

## Manual Setup

```shell
# if you start without virtual environment
pyenv local 3.6.4
python -m venv venv
source ./venv/bin/activate

# install packages
pip install --upgrade pip
pip install -r requirements.txt

#install new package
pip freeze > requirements.txt

#run 
python app/main.py

# run dev server
FLASK_ENV=development python -m flask run

# run within project
cd app
FLASK_ENV=development FLASK_APP=app/main.py python -m flask run

# Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)

# run unit tests via pytest
pytest

# run test with summary of failed(x), passed(X), skipped(s)
pytest -rxXs

# run rabbitmq docker
docker run -d --hostname my-rabbit --name some-rabbit -p 15672:15672 -p 4369:4369 -p 5671:5671 -p 5672:5672 rabbitmq:3-management
# connect to amqp://guest:guest@127.0.0.1:5672
# see management in browser at 127.0.0.1:15672

# run celery
source ./venv/bin/activate
cd app
celery worker -A main.celery --loglevel=info
```


