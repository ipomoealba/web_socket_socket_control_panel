import time

from celery import task
from util.data_sender import DataSender


@task()
def sendData(ip, port, data):
    sender = DataSender(ip, port)
    sender.connect()
    sender.send(data)
    sender.close()
