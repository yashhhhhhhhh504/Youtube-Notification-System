import pika
import sys
import json

class YoutuberPublisher:
    def __init__(self, youtuber_name, video_name):
        self.youtuber_name = youtuber_name
        self.video_name = video_name
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange='logs', exchange_type='fanout')

    def publish_video(self):
        message = json.dumps({'youtuber': self.youtuber_name, 'video_name': self.video_name})
        self.channel.basic_publish(exchange='logs', routing_key='', body=message)
        print("SUCCESS: Video published to the server.")

    def close_connection(self):
        self.connection.close()

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python Youtuber1.py [youtuber_name] [video_name]")
        sys.exit(1)

    youtuber_name = sys.argv[1]
    video_name = ' '.join(sys.argv[2:])

    youtuber_publisher = YoutuberPublisher(youtuber_name, video_name)
    youtuber_publisher.publish_video()
    youtuber_publisher.close_connection()
