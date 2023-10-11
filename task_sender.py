import pika


class TaskSender:
    class BrokerConnectionError(Exception):
        pass

    class BrokerMessageError(Exception):
        pass

    def __init__(self):
        self.credentials = pika.credentials.PlainCredentials(username='igor', password='343877')
        self.__connect()

    def __connect(self):
        try:
            self.connection = pika.BlockingConnection(
                pika.ConnectionParameters(host='localhost', port=5672, credentials=self.credentials))
            self.channel = self.connection.channel()
        except pika.exceptions.AMQPConnectionError:
            raise self.BrokerConnectionError("Cant connect to broker")

    def __create_queue(self):
        try:
            self.channel.queue_declare(queue='gmaps', durable=True)
        except Exception:
            raise self.BrokerMessageError("Cant connect to channel")

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
        except pika.exception.BodyTooLong:
            raise self.BrokerMessageError("Data length too long")

    def __del__(self):
        try:
            self.connection.close()
        except AttributeError:
            pass
