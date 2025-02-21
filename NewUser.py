import pika
import sys
import json

class User:
    def __init__(self, username):
        self.username = username
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=f'{username}_queue')

    def updateSubscription(self, youtuber_name, subscribe):
        # Construct the request message
        request = {
            "user": self.username,
            "youtuber": youtuber_name,
            "subscribe": subscribe
        }
        # Publish the request to the user queue
        self.channel.basic_publish(exchange='', routing_key=f'{self.username}_queue', body=json.dumps(request))
        print("SUCCESS: Subscription updated")

    def receiveNotifications(self):
        def callback(ch, method, properties, body):
            print(f"New Notification: {body.decode()}")

        # Start consuming messages from the user queue
        self.channel.basic_consume(queue=f'{self.username}_queue', on_message_callback=callback, auto_ack=True)
        print('Waiting for notifications...')
        self.channel.start_consuming()

if __name__ == "__main__":
    # Parse command line arguments: username and optional action and YouTuber name
    username = sys.argv[1]
    action = sys.argv[2] if len(sys.argv) > 2 else None
    youtuber_name = sys.argv[3] if len(sys.argv) > 3 else None
    
    # Create a User instance
    user = User(username)

    # Perform action if specified
    if action:
        subscribe = True if action == 's' else False
        user.updateSubscription(youtuber_name, subscribe)

    # Receive notifications
    user.receiveNotifications()
