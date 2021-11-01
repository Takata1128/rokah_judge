FROM python:3.7

RUN mkdir /code
WORKDIR /code

ADD app /code/app

RUN pip install --upgrade pip --no-cache-dir
RUN pip install -r /code/app/requirements.txt --no-cache-dir
RUN apt update && apt install -y git

EXPOSE 9876
WORKDIR /code/app

ENTRYPOINT [ "gunicorn", "wsgi:app" ]
CMD [ "-c", "gunicorn_settings.py" ]