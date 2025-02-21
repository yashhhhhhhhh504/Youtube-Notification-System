# YouTube Notification System

This system enables users to subscribe to their favorite YouTubers and receive notifications when those YouTubers publish new videos. It uses RabbitMQ as a message broker to facilitate communication between various components.

## Components Involved

### 1. `user.py`
- Client-side module representing individual users.
- Users can subscribe/unsubscribe to YouTubers.
- Each user has a personal message queue to receive notifications.

### 2. `youtuber.py`
- Module simulating YouTubers.
- Allows "YouTubers" to announce (publish) new videos.

### 3. `YoutubeServer.py`
- Central server component using RabbitMQ.
- Processes subscription requests from users.
- Maintains a registry of YouTubers and subscribed users.
- Routes new video notifications from publishers (YouTubers) to subscribed users.

## Running the Files

### 1. Start the YouTube Server:
```bash
python YoutubeServer.py
```

### 2. Run User Clients:
```bash
python user.py <username>
python user.py <another_username>
```

### 3. Simulate Subscriptions:
```bash
python user.py <username> s <youtuber_name>  # Subscribe
python user.py <username> u <youtuber_name>  # Unsubscribe
```

### 4. Simulate YouTuber Video Release:
```bash
python youtuber.py <youtuber_name> <video_name>
```

## Dependencies
Ensure you have RabbitMQ installed and running before executing the scripts.

## License
This project is licensed under the MIT License.

