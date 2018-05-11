
#!/usr/bin/env python
# -*- coding: utf-8 -*-
from websocket import create_connection

import socket
import threading

url = "ws://localhost:8000/ws/status_update/status/"


def replySocket(ip, port, name, message, data_type="reply"):
    ws = create_connection("ws://localhost:8000/ws/status_update/status/")
    ws.send('{"message":"' + message.replace('"', '\\"') + '",  "type": "' + data_type + '" , "ip":"' + ip +
            '","port": "'+port+'", "name": "'+name+'"}')
    print("Sent")
    print("Reeiving...")
    result = ws.recv()
    print("Received '%s'" % result)
    ws.close()


class ClientThread(threading.Thread):
    def __init__(self, clientAddress, clientsocket):
        threading.Thread.__init__(self)
        self.csocket = clientsocket
        print ("New connection added: ", clientAddress)

    def run(self):
        print ("Connection from : ", clientAddress)
        #self.csocket.send(bytes("Hi, This is from Server..",'utf-8'))
        ip, port = clientAddress

        while True:
            data = self.csocket.recv(2048)
            msg = data.decode().replace('\n', '').replace('""', '\\"')
            if msg is '':
                break
            else:
                replySocket(ip, str(port), "Socket Server",
                            msg, "socket")
            print ("from client", msg)
            self.csocket.send(bytes(msg, 'UTF-8'))
        self.csocket.close()
        print ("Client at ", clientAddress, " disconnected...")


LOCALHOST = "0.0.0.0"
PORT = 8088
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((LOCALHOST, PORT))
print("Server started")
print("Waiting for client request..")
print("Listen in: " + LOCALHOST, PORT)

while True:
    server.listen(1)
    clientsock, clientAddress = server.accept()
    newthread = ClientThread(clientAddress, clientsock)
    newthread.start()
