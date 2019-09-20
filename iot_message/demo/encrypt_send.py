import socket
from iot_message.message import Message
from iot_message.cryptor.base64 import Cryptor as B64
from iot_message.cryptor.plain import Cryptor as Plain
from iot_message.cryptor.aes_sha1 import Cryptor as AES

address = ('192.168.1.255', 5053)
# address = ('192.168.43.255', 5053)

Message.chip_id = 'pc'
Message.node_name = 'Turkusik'
Message.add_encoder(B64())
Message.add_encoder(Plain())
Message.add_encoder(AES(
    'abcdef2345678901', '2345678901abcdef', '0123456789abcdef', 'mypassphrase'
))
message = Message()
message.set({
    'event': 'channel.off',
    'parameters': {
        'channel': 0
    },
    'targets': ['ALL']
})

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
message.encoder = 2
print(message)
s.sendto(bytes(message), address)
