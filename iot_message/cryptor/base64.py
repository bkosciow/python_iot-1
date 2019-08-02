import base64
import json
from iot_message.abstract.cryptor_interface import CryptorInterface


class Cryptor(CryptorInterface):
    name = "message.base64"

    def encrypt(self, message):
        msg = json.dumps(message.data)
        encoded_msg = base64.b64encode(msg.encode())
        message.set({
            'event': 'message.base64',
            'parameters': [encoded_msg.decode()],
            'response': ''
        })

    def decrypt(self, message):
        pass
