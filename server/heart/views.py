import requests

import json
#  from server.settings import SOCKET_SERVER_PORT, SOCKET_SERVER_IP
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Device, Command, Status
from django.http import JsonResponse
from django.utils.safestring import mark_safe
from .tasks import sendData

# chat/views.py
#  from django.shortcuts import render


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def device_handshaker(request):
    device_name = request.GET.get("device_id", False)
    device_ip = get_client_ip(request)
    try:
        device_exist = Device.objects.get(name=device_name)
        device_exist.ip = device_ip
        device_exist.save()
        print("Update Ip: ", device_ip, " for ", "device_name")
    except Exception:
        device = Device(name=device_name, ip=device_ip)
        device.save()
        print("Create new Device: ", device_name, " ip: ", device_ip)
    return HttpResponse("got")


def control_panel(request):
    ip = request.POST.get("ip", False)
    port = request.POST.get("port", False)
    command = request.POST.get("command", False)
    devices = Device.objects.all()
    commands = Command.objects.all()
    status = Status.objects.all()

    if ip and port and command:
        print(ip, port, command)
        sendData.delay(
            ip,
            port,
            command
        )
        return render(request, "control_panel.html", {
            "status": "success",
            "devices": devices,
        })
    else:
        return render(request, "control_panel.html", {
            "devices": devices,
            "commands": commands,
            "statuses": status
        })


def force_change_status(request):
    device_id = request.GET.get("device", False)
    command_f = request.GET.get("command", False)
    if device_id and command_f:
        device = Device.objects.get(id=device_id)
        command = Command.objects.get(id=command_f.split("||")[1])
        Status.objects.filter(device__id=device_id).update(
            command=command_f.split("||")[1])
        if "Unity" in command_f:
            print("send",  device.ip, "88", command.command)
            sendData.delay(device.ip, device.port, command.command)
        else:
            result = requests.get(
                "http://" + device.ip + "/" + command.command)
            print(result)
        return HttpResponseRedirect("/")


def ajax_update_device_status(request):
    device_id = request.GET.get("device_id", False)
    command_id = request.GET.get("command_id", False)
    Status.objects.filter(device__id=device_id).update(
        command=command_id)
    status = Status.objects.get(device__id=device_id)
    data = {
        'status_id': status.id,
        'status_update': status.updated,
        'status_command': Command.objects.get(id=command_id).name
    }
    return JsonResponse(data)


def rule_check(request):
    ip = request.GET.get("ip", False)
    port = request.GET.get("port", False)
    command = request.GET.get("message", False)
