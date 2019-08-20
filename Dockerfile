FROM tiangolo/uwsgi-nginx-flask:python3.7

COPY ./app /app
COPY ./uwsgi.ini /app/uwsgi.ini

COPY ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt