import socket


class DataSender(object):
    def __init__(self, ip, port):
        super(DataSender, self).__init__()
        self.ip = ip
        self.port = int(port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        self.sock.connect((self.ip, self.port))

    def send(self, data):
        self.sock.send(data.encode('utf-8'))
        reply = self.sock.recv(1024).decode("utf-8")
        return reply
        #  print(str.decode("utf-8"))

    def close(self):
        self.sock.close()


if __name__ == "__main__":
    sender = DataSender("127.0.0.1", 8080)
    sender.connect()
    sender.send('{"hi": "ho"}')
    sender.close()
