import socket
from iot_message.message import Message
from iot_message.cryptor.base64 import Cryptor as B64

address = ('192.168.1.255', 5053)
address = ('192.168.43.255', 5053)


Message.chip_id = 'pc'
Message.node_name = 'Turkusik'
message = Message()
message.encoder = B64()
message.set({
    'event': 'channel.off',
    'parameters': {
        'channel': 0
    },
    'targets': ['ALL']
})

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
message.encrypt()
print(message)
s.sendto(bytes(message), address)
