import socket
from iot_message.message import Message

address = ('192.168.1.255', 5053)

message = Message()
message.set({
    'event': 'channel.off',
    'parameters': {
        'channel': 0
    },
    'targets': ['node-north']
})

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
print(message)
s.sendto(bytes(message), address)
