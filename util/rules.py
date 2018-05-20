import traceback
from heart.models import Command, Rule, Restrict, Status

from util.websocket_help import replySocket


def automator(ip, port, message, device_name="UnKnown"):
    try:

        do_next_step = False
        if ip == '0.0.0.0' and device_name == "Unknown":
            replySocket("localhost",
                        "8000",
                        "Automator -> Cannot Found The Device",
                        "None",
                        data_type="return")

        else:
            pre_step_command = Command.objects.filter(
                command__contains=message.replace(" ", ""),
                device__ip=ip)
            if pre_step_command.count() > 0:
                pre_step_command = pre_step_command[0]
                pre_step_device = pre_step_command.device.id
                next_step = Rule.objects.filter(
                device=pre_step_device, pre_step=pre_step_command)
                if next_step.count() > 0:
                    next_step = next_step.first()
                    constrict = Restrict.objects.filter(
                        prerequisites=next_step.next_step)
                    if constrict.count() != 0:
                        status = Status.objects.get(
                            device=next_step.next_step.device)
                        if status.command == constrict.prerequisites:
                            do_next_step = True
                        else:
                            do_next_step = False
                    else:
                        do_next_step = True
            else:
                replySocket("localhost",
                            "8000",
                            "Automator -> There is no next step",
                            "None",
                            data_type="return")

        if do_next_step:
            Status.objects.filter(device=next_step.next_step.device).update(
                command=next_step.next_step)
            if next_step.device.name == 'Unity':
                replySocket(next_step.next_step.device.ip,
                            next_step.next_step.device.port,
                            "Automator -> " + next_step.next_step.device.name,
                            next_step.next_step.command.replace('"', '\\"'),
                            data_type="command")
            else:
                replySocket(
                    next_step.next_step.device.ip,
                    next_step.next_step.device.port,
                    "Automator -> " + next_step.next_step.device.name,
                    next_step.next_step.command, data_type="request")
    except Exception as e:
        replySocket(ip, port, "Automator", traceback.format_exc().replace('"', '\'') , "error")
