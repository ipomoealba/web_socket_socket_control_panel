import requests
from celery import task
from util.data_sender import DataSender
from util.websocket_help import replySocket
import traceback 

@task()
def sendRequest(ip, port, message, name="Task Return"):
    try:
        url = "http://" + ip + ":" + port + "/?" + message
        print(url)
        result = requests.get(url, timeout=15)
        message = result
        replySocket(ip, port, name, message, "return")
    except Exception as e:
        replySocket(ip, port, name, traceback.format_exc().replace('"', '\''), "error")


@task()
def sendData(ip, port, data, name="Task Return"):
    try:
        sender = DataSender(ip, port)
        sender.connect()
        result = sender.send(data)
        sender.close()
        replySocket(ip, port, name, result, "return")
    except Exception as e:
        replySocket(ip, port, name, traceback.format_exc().replace('"', '\''), "error")
