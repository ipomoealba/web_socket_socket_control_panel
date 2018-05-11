import requests
from celery import task
from util.data_sender import DataSender
from util.websocket_help import replySocket


@task()
def sendRequest(ip, port, message, name="Task Return"):
    try:
        result = requests.get("http://" + ip + ":" +
                              port + "/" + message, timeout=0.001)
        message = result
        replySocket(ip, port, name, message, "return")
    except Exception as e:
        message = str(e)
        replySocket(ip, port, name, message, "error")


@task()
def sendData(ip, port, data, name="Task Return"):
    try:
        sender = DataSender(ip, port)
        sender.connect()
        result = sender.send(data)
        sender.close()
        replySocket(ip, port, name, result, "return")
    except Exception as e:
        replySocket(ip, port, name, str(e), "error")
