import pika

class YoutubeServer:
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange='logs', exchange_type='fanout')

        self.channel.queue_declare(queue='user_requests')
        self.channel.queue_declare(queue='youtuber_notifications')

        self.channel.queue_bind(exchange='logs', queue='user_requests')
        self.channel.queue_bind(exchange='logs', queue='youtuber_notifications')

        self.youtubers = {}
        self.users = {}

    def notify_users(self, youtuber, video_name):
        for user, subscriptions in self.users.items():
            if youtuber in subscriptions:
                message = f'Notification: {youtuber} just uploaded {video_name}'
                self.channel.basic_publish(exchange='logs',
                                           routing_key='',
                                           body=message)
                print(f"Notification sent to {user}: {message}")

    def consume_user_requests(self, ch, method, properties, body):
        username = body.decode()
        if username not in self.users:
            self.users[username] = set()
            print(f'{username} logged in')
        else:
            print(f'{username} already logged in')
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def consume_youtuber_notifications(self, ch, method, properties, body):
        bod = body.decode().split('"')
        youtuber, video_name = bod[3], bod[7]
        if youtuber not in self.youtubers:
            self.youtubers[youtuber] = []
        self.youtubers[youtuber].append(video_name)
        print(f'{youtuber} uploaded {video_name}')
        self.notify_users(youtuber, video_name)
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def start_consuming(self):
        self.channel.basic_consume(queue='user_requests',
                                    on_message_callback=self.consume_user_requests)
        self.channel.basic_consume(queue='youtuber_notifications',
                                    on_message_callback=self.consume_youtuber_notifications)

        print(' [*] Waiting for messages. To exit press CTRL+C')
        self.channel.start_consuming()

if __name__ == "__main__":
    youtube_server = YoutubeServer()
    youtube_server.start_consuming()
