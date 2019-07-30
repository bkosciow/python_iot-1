#!/usr/bin/python3
# -*- coding: utf-8 -*-
#pylint: skip-file

from nose.tools import assert_equal
from nose.tools import assert_not_equal
from nose.tools import assert_is_instance
from nose.tools import assert_raises
import iot_message.exception as ex
import json

__author__ = 'Bartosz Kościów'

import iot_message.message as message
import iot_message.factory as factory


class TestMessageFactory(object):
    def test_create_empty_message(self):
        msg = factory.MessageFactory.create()
        assert_is_instance(msg, message.Message)

    def test_decode_message(self):
        message.Message.node_name = 'this'
        input = """{"protocol": "iot:1", "node": "node_name", "chip_id": "aaa", "event": "channel.on", "parameters": {"channel": 0}, "response": "", "targets": ["this"]}"""
        msg = factory.MessageFactory.create(input)

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

    def test_raise_JsonException_on_decode_faulty_message(self):
        input = """{"protocol" "iot:1", "node": "node_name", "chip_id": "aaa", "event": "channel.on", "parameters": {"channel": 0}, "response": "", "targets": ["node-north"]}"""
        assert_raises(ex.JsonException, factory.MessageFactory.create, input)

    def test_accept_message_target_all(self):
        input = """{"protocol": "iot:1", "node": "node_name", "chip_id": "aaa", "event": "channel.on", "parameters": {"channel": 0}, "response": "", "targets": ["ALL"]}"""
        msg = factory.MessageFactory.create(input)
        assert_not_equal(msg, None)

    def test_accept_message_target_this(self):
        message.Message.node_name = 'this'
        input = """{"protocol": "iot:1", "node": "node_name", "chip_id": "aaa", "event": "channel.on", "parameters": {"channel": 0}, "response": "", "targets": ["this"]}"""
        msg = factory.MessageFactory.create(input)
        assert_not_equal(msg, None)

    def test_reject_message_not_a_target(self):
        message.Message.node_name = 'this'
        input = """{"protocol": "iot:1", "node": "node_name", "chip_id": "aaa", "event": "channel.on", "parameters": {"channel": 0}, "response": "", "targets": ["that"]}"""
        msg = factory.MessageFactory.create(input)
        assert_equal(msg, None)
