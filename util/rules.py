from heart.models import Device, Command, Rule
from util.websocket_help import replySocket


def automator(ip, port, message, device_name="UnKnown"):
    try:
        pre_step_command = Command.objects.get(
            command__contains=message.replace(" ", ""))
        pre_step_device = pre_step_command.device.id
        next_step = Rule.objects.filter(
            device=pre_step_device, pre_step=pre_step_command)[0]

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
