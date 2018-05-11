from websocket import create_connection

def replySocket(ip, port, name, message, data_type="reply"):
    ws = create_connection("ws://localhost:8000/ws/status_update/status/")
    ws.send('{"message":"' + message + '",  "type": "' + data_type + '" , "ip":"' + ip +
            '","port": "'+port+'", "name": "'+name+'"}')
    print("Sent")
    print("Reeiving...")
    result = ws.recv()
    print("Received '%s'" % result)
    ws.close()

