from tradingviewalerts.forwarders.base import BaseForwarder
from os import environ
import aio_pika
import ujson
import asyncio

AMQP_CONN_STRING = environ.get('AMQP_CONN_STRING')
AMQP_QUEUE = environ.get('AMQP_QUEUE')


class RabbitMQForwarder(BaseForwarder):
    async def send_notification(self, message: dict):
        connection: aio_pika.Connection = await aio_pika.connect(AMQP_CONN_STRING,
                                                                 loop=asyncio.get_event_loop())
        channel: aio_pika.Channel = await connection.channel()
        await channel.declare_queue(name=AMQP_QUEUE,
                                    auto_delete=True)

        amqp_message = aio_pika.Message(body=ujson.dumps(message).encode())

        await channel.default_exchange.publish(message=amqp_message,
                                               routing_key=AMQP_QUEUE)

        await connection.close()
