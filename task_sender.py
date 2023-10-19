import pika
from google_maps_parser_api.settings import PIKA_USERNAME, PIKA_PASSWORD, PIKA_HOST, PIKA_PORT
import logging
from load_logging_conf import configure_logging

configure_logging()
logger = logging.getLogger(f"{__name__}_TaskSender")


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
            logger.debug("Connected to rabbitmq")
        except pika.exceptions.AMQPConnectionError as e:
            logger.error("Cant connect ot rabbitmq", exc_info=True)
            raise self.BrokerConnectionError(f"Can't connect to broker: {e}")

    def __create_queue(self):
        try:
            self.channel.queue_declare(queue='gmaps', durable=True)
            logger.debug("Created rabbitmq queue")
        except pika.exceptions.ChannelError as e:
            logger.error("Cant create rabbitmq queue", exc_info=True)
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
            logger.debug(f"Send task to rabbitmq {task}")
            return True
        except pika.exceptions.BodyTooLong:
            logger.error("Cant send task to rabbitmq", exc_info=True)
            raise self.BrokerMessageError("Data length too long")
        except pika.exceptions.AMQPError as e:
            logger.error("Error while sending message to rabbitmq", exc_info=True)
            raise self.BrokerMessageError(f"Error while sending message: {e}")

    def __del__(self):
        try:
            self.connection.close()
            logger.debug("Close connection to rabbitmq")
        except AttributeError:
            pass
