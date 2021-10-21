FROM python:3.7

RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/requirements.txt
ADD entrypoint.sh /code/entrypoint.sh
ENV DATABASE_URI "mysql://root:password@mysql:3306"
ENV DB_HOST "mysql"
ENV DB_USER "root"
ENV DB_PASSWORD "password"
ENV DB_NAME "rokah_judge"
RUN apt update && apt install -y build-essential rabbitmq-server
RUN python3 -m pip install -r requirements.txt

# CMD ["/bin/bash"]
CMD [ "/code/entrypoint.sh" ]
