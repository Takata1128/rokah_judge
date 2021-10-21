#!/usr/bin/env python
import pika
import sys
import os
import json
from judge import judge


def main():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='rabbitmq'))
    channel = connection.channel()

    channel.queue_declare(queue='judge')

    def callback(ch, method, properties, body):
        print(" [x] Received %r" % body)
        params = json.loads(body)
        judge(**params)

    channel.basic_consume(
        queue='judge', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
