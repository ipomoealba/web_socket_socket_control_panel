# chat/consumers.py
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .tasks import sendData, sendRequest
from util.rules import automator, replySocket
from heart.models import Rule
import json


class StatusConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        print(text_data)
        text_data_json = ''
        
        try:
            text_data_json = json.loads(text_data)
        except Exception as e:
            print(e)
            print("Data Type Error! Not Json Format")
        
        if text_data_json:
            data_type = text_data_json['type']
            message = text_data_json['message']
            ip = text_data_json['ip']
            name = text_data_json['name']
            port = text_data_json['port']
            message_header = ''
            if data_type == 'command':
                message_header = '[Send Socket]'
                sendData.delay(
                    ip,
                    port,
                    message
                )
                automator(ip, port, message)
            elif data_type == 'request':
                message_header = '[Send Request]'
                sendRequest.delay(ip, port, message)
                automator(ip, port, message)
            elif data_type == 'socket':
                message_header = '[Get Socket Message]'
                try:
                    automator(ip, port, message)
                except:
                    pass
            elif data_type == 'error':
                message_header = '[!!!]'
            elif data_type == 'return':
                message_header = '[Return]'

        else:
            message_header = 'Json Type Error'
            message = text_data
            ip = "localhost"
            port = "0000"
            name = "System"
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message_header + " " + message,
                'ip': ip,
                'name': name,
                'port': port

            }
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']
        ip = event['ip']
        name = event['name']
        port = event['port']
        # Send message to WebSocket

        self.send(text_data=json.dumps({
            'message': message,
            'ip': ip,
            'name': name,
            'port': port
        }))
