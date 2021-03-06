import requests
from celery import task
from util.data_sender import DataSender
from util.websocket_help import replySocket
import traceback
from pygame import mixer


@task
def playMusic(link):
    mixer.pre_init(48000, -16, 1, 512)
    mixer.init()
    mixer.music.load(link)
    mixer.music.play()


@task()
def replySocketAsync(ip, port, name, message, data_type):
    replySocket(ip, port, name, message, data_type)


@task()
def sendRequest(ip, port, message, name="Task Return"):
    try:
        url = "http://" + ip + ":" + port + "/?" + message
        result = requests.get(url)
        message = result
        replySocket(ip, port, name, message, "return")
    except Exception as e:
        replySocket(ip, port, name, traceback.format_exc().replace(
            '"', '\''), "error")


@task()
def sendData(ip, port, data, name="Task Return"):
    try:
        sender = DataSender(ip, port)
        sender.connect()
        result = sender.send(data)
        sender.close()
        replySocket(ip, port, name, result, "return")
    except Exception as e:
        replySocket(ip, port, name, traceback.format_exc().replace(
            '"', '\''), "error")
