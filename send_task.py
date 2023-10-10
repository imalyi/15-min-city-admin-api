import pika


class TaskSender:
    def __init__(self):
        #TODO  how to store sensetive info like passwords and login???
        self.credentials = pika.credentials.PlainCredentials(username='igor', password='343877')
        self.__connect()

    def __connect(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost', port=5672, credentials=self.credentials))
        self.channel = self.connection.channel()

    def __create_queue(self):
        self.channel.queue_declare(queue='gmaps', durable=True)

    def send(self, task: str) -> bool:
        self.__create_queue()
        self.channel.basic_publish(
            exchange='',
            routing_key='gmaps',
            body=task,
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            ))
        return True

    def __del__(self):
        self.connection.close()
