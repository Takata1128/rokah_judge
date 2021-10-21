import pika, json

from pika.amqp_object import Properties


def push(**kwargs):
    conn_params = pika.ConnectionParameters(host="rabbitmq")
    connection = pika.BlockingConnection(conn_params)
    channel = connection.channel()

    channel.queue_declare(queue="judge")
    properties = pika.BasicProperties(content_type="application/json", delivery_mode=2)
    channel.basic_publish(
        exchange="", routing_key="judge", body=json.dumps(kwargs), properties=properties
    )
    connection.close()
