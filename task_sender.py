import pika
from google_maps_parser_api.settings import PIKA_USERNAME, PIKA_PASSWORD, PIKA_HOST, PIKA_PORT


class TaskSender:
    class BrokerConnectionError(Exception):
        pass

    class BrokerMessageError(Exception):
        pass

    def __init__(self):
        self.credentials = pika.PlainCredentials(username=PIKA_USERNAME, password=PIKA_PASSWORD)
        self.__connect()

    def __connect(self):
        try:
            self.connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=PIKA_HOST, port=PIKA_PORT, credentials=self.credentials))
            self.channel = self.connection.channel()
        except pika.exceptions.AMQPConnectionError as e:
            raise self.BrokerConnectionError(f"Can't connect to broker: {e}")

    def __create_queue(self):
        try:
            self.channel.queue_declare(queue='gmaps', durable=True)
        except pika.exceptions.ChannelError as e:
            raise self.BrokerMessageError(f"Can't create queue: {e}")

    def send(self, task: str) -> bool:
        try:
            self.__create_queue()
            self.channel.basic_publish(
                exchange='',
                routing_key='gmaps',
                body=task,
                properties=pika.BasicProperties(
                    delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
                ))
            return True
        except pika.exceptions.BodyTooLong:
            raise self.BrokerMessageError("Data length too long")
        except pika.exceptions.AMQPError as e:
            raise self.BrokerMessageError(f"Error while sending message: {e}")

    def __del__(self):
        try:
            self.connection.close()
        except AttributeError:
            pass
