import requests

from server.settings import SOCKET_SERVER_PORT, SOCKET_SERVER_IP
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Device, Command, Status
from django.http import JsonResponse

from .tasks import sendData


def rule(device, flag):
    if device == "unity":
        if flag == "":
            pass


def unity_test(request):
    return JsonResponse({"status": "OK"})


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def django_view(request):
    # get the response from the URL
    response = requests.get('http://example.com')
    return response.headers


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


def control(request):
    commands = Command.objects.all()
    return render(request, "arduino-control-panel.html", {
        "commands": commands,
    })


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
    device = request.GET.get("device", False)
    command = request.GET.get("command", False)
    if device and command:
        print(device, command)
        Status.objects.filter(device__id=device).update(command=command.split("||")[1])
        #  return JsonResponse({"status": "succcess"})
        return HttpResponseRedirect("/")


def send(request):
    return HttpResponseRedirect("/path/")
