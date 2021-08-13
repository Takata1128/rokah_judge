FROM python:3.7

RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/requirements.txt
ADD entrypoint.sh /code/entrypoint.sh
ADD receive.py /code/receive.py
ENV DATABASE_URI "postgresql://postgres:postgres@docker_postgres:5432"
RUN apt update && apt install -y build-essential rabbitmq-server
RUN python3 -m pip install -r requirements.txt

CMD ["/bin/bash"]
# CMD [ "/code/entrypoint.sh" ]
