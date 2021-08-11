FROM python:3.7

RUN mkdir /code
WORKDIR /code
ADD receive.py /code/receive.py
ADD entrypoint.sh /code/entrypoint.sh
RUN apt update && apt install -y build-essential rabbitmq-server
RUN python3 -m pip install pika --upgrade

CMD [ "/code/entrypoint.sh" ]
