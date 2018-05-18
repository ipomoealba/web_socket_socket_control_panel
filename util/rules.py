from heart.models import Command, Rule, Restrict, Status

from util.websocket_help import replySocket


def automator(ip, port, message, device_name="UnKnown"):
    try:

        do_next_step = False
        if ip == '0.0.0.0' and device_name == "Unknown":
            print("Cannot Detect device")

        else:
            pre_step_command = Command.objects.filter(
                command__contains=message.replace(" ", ""),
                device__ip=ip).first()
            pre_step_device = pre_step_command.device.id
            next_step = Rule.objects.filter(
                device=pre_step_device, pre_step=pre_step_command)[0]

            constrict = Restrict.objects.filter(
                prerequisites=next_step.next_step)
            if constrict.count() != 0:
                status = Status.objects.get(device=next_step.next_step.device)
                if status.command == constrict.prerequisites:
                    do_next_step = True
                else:
                    do_next_step = False
            else:
                do_next_step = True

        if do_next_step:
            Status.objects.filter(device=next_step.next_step.device).update(
                command=next_step.next_step)
            if next_step.device.name == 'Unity':
                replySocket(next_step.next_step.device.ip,
                            next_step.next_step.device.port,
                            "Automator -> " + next_step.next_step.device.name,
                            next_step.next_step.command,
                            data_type="command")
            else:
                replySocket(
                    next_step.next_step.device.ip,
                    next_step.next_step.device.port,
                    "Automator -> " + next_step.next_step.device.name,
                    next_step.next_step.command, data_type="request")
    except Exception as e:
        replySocket(ip, port, "Automator", e, "error")
