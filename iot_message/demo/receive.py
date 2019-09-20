import socket
from iot_message.cryptor.base64 import Cryptor as B64
from iot_message.cryptor.aes_sha1 import Cryptor as AES
from iot_message.message import Message
import iot_message.factory as factory

ip_address = '0.0.0.0'
port = 5053
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
s.settimeout(0.5)
s.bind((ip_address, port))

Message.chip_id = 'pc'
Message.node_name = 'Turkusik'
Message.add_decoder(B64())
Message.add_decoder(AES(
    'abcdef2345678901', '2345678901abcdef', '0123456789abcdef', 'mypassphrase'
))
try:
    while True:
        try:
            data, address = s.recvfrom(65535)
            msg = factory.MessageFactory.create(data)
            # if msg.data["node"] == "node-north":
            print(msg)
        except socket.timeout:
            pass
finally:
    s.close()
