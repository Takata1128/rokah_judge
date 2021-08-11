FROM python:3.7

RUN mkdir /code
WORKDIR /code

ADD app /code/app
ADD entrypoint.sh /code/entrypoint.sh

RUN pip install --upgrade pip --no-cache-dir
RUN pip install -r /code/app/requirements.txt --no-cache-dir
RUN apt update && apt install -y git postgresql-client

EXPOSE 5000
ENV FLASK_APP "/code/app/run.py"
CMD ["/code/entrypoint.sh"]