#!/usr/bin/python3
# -*- coding: utf-8 -*-
#pylint: skip-file

from nose.tools import assert_equal
from nose.tools import assert_not_equal
from nose.tools import assert_is_instance
import iot_message.factory as factory
from nose.tools import assert_raises
import iot_message.exception as ex
import json
from iot_message.cryptor.base64 import Cryptor as B64
from iot_message.cryptor.plain import Cryptor as Plain
from unittest.mock import MagicMock

__author__ = 'Bartosz Kościów'

import iot_message.message as message


class TestMessage(object):
    def setUp(self):
        message.Message.chip_id = 'pc'
        message.Message.node_name = 'this'
        message.Message.drop_unencrypted = False
        message.Message.encoders = []
        message.Message.decoders = {}

    def test_init_with_chip_id(self):
        msg = message.Message()
        assert_equal(msg.chip_id, 'pc')

    def test_init_with_node_name(self):
        message.Message.node_name = 'miau_too'
        msg = message.Message()
        assert_equal(msg.node_name, 'miau_too')

    def test_init_without_chip_id(self):
        message.Message.chip_id = None
        msg = message.Message()
        assert_not_equal(msg.chip_id, None)

    def test_init_without_node_name(self):
        message.Message.node_name = None
        msg = message.Message()
        assert_is_instance(msg.node_name, str)

    def test_initialize_empty_data(self):
        msg = message.Message()
        msg.set({})
        data = {
            'protocol': msg.protocol,
            'node': msg.node_name,
            'chip_id': msg.chip_id,
            'event': '',
            'parameters': {},
            'response': '',
            'targets': [
                'ALL'
            ]
        }
        assert_equal(msg.data, data)

    def test_initialize_data(self):
        msg = message.Message()
        msg.set({
            'event': 'event.test',
            'parameters': {
                'is_x': '1'
            }
        })
        data = {
            'protocol': msg.protocol,
            'node': msg.node_name,
            'chip_id': msg.chip_id,
            'event': 'event.test',
            'parameters': {
                'is_x': '1'
            },
            'response': '',
            'targets': [
                'ALL'
            ]
        }

        assert_equal(msg.data, data)

    def test_update_data(self):
        msg = message.Message()
        msg.set({
            'event': 'event.test',
            'parameters': {
                'is_x': '1'
            }
        })
        msg.set({
            'targets': ['self'],
        })
        data = {
            'protocol': msg.protocol,
            'node': msg.node_name,
            'chip_id': msg.chip_id,
            'event': 'event.test',
            'parameters': {
                'is_x': '1'
            },
            'response': '',
            'targets': [
                'self'
            ]
        }

        assert_equal(msg.data, data)

    def test_decoder_not_found(self):
        message.Message.node_name = 'Turkusik'
        inp = {
            "event": "message.notfound",
            "parameters": ["eyJwcm90b2NvbCI6ICJpb3Q6MSIsICJub2RlIjogIlR1cmt1c2lrIiwgImNoaXBfaWQiOiAicGMiLCAiZXZlbnQiOiAiY2hhbm5lbC5vbiIsICJwYXJhbWV0ZXJzIjogeyJjaGFubmVsIjogMH0sICJyZXNwb25zZSI6ICIiLCAidGFyZ2V0cyI6IFsiVHVya3VzaWsiXX0="],
            "response": "",
            "targets": ["Turkusik"]
        }
        msg = message.Message()
        msg.set(inp)
        assert_raises(ex.DecryptNotFound, msg.decrypt)

    def test_allow_plain_message(self):
        inp = {"protocol": "iot:1", "node": "node_name", "chip_id": "aaa", "event": "channel.on", "parameters": {"channel": 0}, "response": "", "targets": ["this"]}
        msg = message.Message()
        msg.set(inp)
        msg.decrypt()
        data = {
            'protocol': 'iot:1',
            'node': 'node_name',
            'chip_id': 'aaa',
            'event': 'channel.on',
            'parameters': {'channel': 0},
            'response': '',
            'targets': ['this']
        }

        assert_equal(bytes(msg), json.dumps(data).encode())

    def test_drop_plain_message(self):
        message.Message.drop_unencrypted = True
        message.Message.add_decoder(B64())
        inp = {"protocol": "iot:1", "node": "node_name", "chip_id": "aaa", "event": "channel.on", "parameters": {"channel": 0}, "response": "", "targets": ["this"]}
        msg = message.Message()
        msg.set(inp)
        msg.decrypt()

        assert_equal(msg.data, None)

    def test_exception_when_decoders_empty_and_crypt_required(self):
        message.Message.drop_unencrypted = True
        inp = {"protocol": "iot:1", "node": "node_name", "chip_id": "aaa", "event": "channel.on", "parameters": {"channel": 0}, "response": "", "targets": ["this"]}
        msg = message.Message()
        msg.set(inp)
        assert_raises(ex.NoDecodersDefined, msg.decrypt)

    def test_add_encoder(self):
        b = B64()
        message.Message.add_encoder(b)
        assert_equal(message.Message.encoders, [b])

    def test_add_encoders(self):
        b = B64()
        p = Plain()
        message.Message.add_encoder(b)
        message.Message.add_encoder(p)
        assert_equal(message.Message.encoders, [b, p])

    def test_first_encoder_should_be_used(self):
        m1 = MagicMock()
        m2 = MagicMock()
        message.Message.add_encoder(m1)
        message.Message.add_encoder(m2)
        msg = message.Message()
        msg.encrypt()
        m2.encrypt.assert_not_called()
        m1.encrypt.assert_called_once()

    def test_second_encoder_should_be_used(self):
        m1 = MagicMock()
        m2 = MagicMock()
        message.Message.add_encoder(m1)
        message.Message.add_encoder(m2)
        msg = message.Message()
        msg.encoder = 1
        msg.encrypt()
        m1.encrypt.assert_not_called()
        m2.encrypt.assert_called_once()