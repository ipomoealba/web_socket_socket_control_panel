import traceback
from heart.models import Command, Rule, Restrict, Status, Device

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
            device_status = Device.objects.filter(ip=ip)
            print(message)
            pre_step_command = Command.objects.filter(
                command__contains=message.replace(" ", ""),
                device__ip=ip)
            #  device_status = Device.objects.filter(
                #  id=pre_step_command[0].device.id)
            replySocket(ip, port, "test", str(pre_step_command), "return")
            device_status.update(standBy=True)
            if pre_step_command.count() > 0:
                pre_step_command = pre_step_command[0]
                pre_step_device = pre_step_command.device.id
                pre_step_device_name = pre_step_command.device.name
                print(pre_step_device_name)
                if "Stele" in pre_step_device_name:
                    if Status.objects.get(device__name="Stele1").command.command == 'STATUS=COMPLETE' and \
                            Status.objects.get(device__name="Stele2").command.command == 'STATUS=COMPLETE':
                        unity = Device.objects.get(name="Unity")
                        replySocket(unity.ip,
                                    unity.port,
                                    "Automator -> " + unity.name,
                                    '{"Stele":1}',
                                    "command")
                    else:
                        replySocket(ip, port, "localhost", "Stele Not Complete", "return")
                else:
                    next_step = Rule.objects.filter(
                        device=pre_step_device, pre_step=pre_step_command)

                    replySocket(ip, port, "test", str(next_step), "return")
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
                        replySocket("localhost", "8000", "Automator -> can not find next step", "None", "return" ) 
            else:
                replySocket("localhost",
                            "8000",
                            "Automator -> Step Command Error",
                            "None",
                            data_type="return")

        if do_next_step:
            Status.objects.filter(device=next_step.next_step.device).update(
                command=next_step.next_step)
            if 'Unity' in next_step.next_step.device.name:
                replySocket(next_step.next_step.device.ip,
                            next_step.next_step.device.port,
                            "Automator -> " + next_step.next_step.device.name,
                            next_step.next_step.command,
                            "command")
            else:
                replySocket(
                    next_step.next_step.device.ip,
                    next_step.next_step.device.port,
                    "Automator -> " + next_step.next_step.device.name,
                    next_step.next_step.command, data_type="request")
    except Exception:
        replySocket(ip, port, "Automator",
                    traceback.format_exc().replace('"', '\''), "error")
