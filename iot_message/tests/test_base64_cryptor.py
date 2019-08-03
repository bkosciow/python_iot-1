#!/usr/bin/python3
# -*- coding: utf-8 -*-
#pylint: skip-file

from nose.tools import assert_equal
from iot_message.cryptor.base64 import Cryptor as B64
from iot_message.message import Message
import base64
import json

__author__ = 'Bartosz Kościów'

import iot_message.factory as factory


class TestCryptorBase64(object):

    def test_encode_message(self):
        Message.chip_id = 'pc'
        Message.node_name = 'Turkusik'
        msg = factory.MessageFactory.create()
        msg.encoder = B64()
        inp = {"event": "channel.on", "parameters": {"channel": 0}, "response": "", "targets": ["node-north"]}
        msg.set(inp)
        msg.encrypt()
        out = json.loads(base64.b64decode(msg.data['parameters'][0]).decode())

        assert_equal(inp["event"], out["event"])
        assert_equal(inp["parameters"], out["parameters"])
        assert_equal(inp["targets"], out["targets"])

    def test_decrypt_message(self):
        Message.chip_id = 'pc'
        Message.node_name = 'Turkusik'
        inp = """{"protocol": "iot:1", "node": "Turkusik", "chip_id": "pc", "event": "message.base64", "parameters": ["eyJwcm90b2NvbCI6ICJpb3Q6MSIsICJub2RlIjogIlR1cmt1c2lrIiwgImNoaXBfaWQiOiAicGMiLCAiZXZlbnQiOiAiY2hhbm5lbC5vbiIsICJwYXJhbWV0ZXJzIjogeyJjaGFubmVsIjogMH0sICJyZXNwb25zZSI6ICIiLCAidGFyZ2V0cyI6IFsiVHVya3VzaWsiXX0="], "response": "", "targets": ["Turkusik"]}"""
        msg = factory.MessageFactory.create(inp)
        msg.add_decoder(B64())
        assert_equal(msg.data["event"], "channel.on")
        assert_equal(msg.data["parameters"], {"channel": 0})
        assert_equal(msg.data["target"], ['Turkusik'])


