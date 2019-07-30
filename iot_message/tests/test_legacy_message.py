#!/usr/bin/python3
# -*- coding: utf-8 -*-
#pylint: skip-file

from nose.tools import assert_equal
from nose.tools import assert_not_equal
import json

__author__ = 'Bartosz Kościów'

import iot_message.legacy_message as message


class TestMessage(object):
    def setUp(self):
        self.msg = message.Message('test-node')

    def test_init_class(self):
        msg = message.Message('test-node', '123')
        assert_equal(msg.node, 'test-node')
        assert_equal(msg.chip_id, '123')

    def test_init_without_chip_id(self):
        msg = message.Message('test-node')
        assert_equal(msg.node, 'test-node')
        assert_equal(msg.chip_id, msg._chip_id)

    def test_prepare_message(self):
        msg = self.msg.prepare_message()
        result = {
            'protocol': 'iot:1',
            'node': self.msg._node,
            'chip_id': self.msg._chip_id,
            'event': '',
            'parameters': {},
            'response': '',
            'targets': [
                'ALL'
            ]
        }

        assert_equal(msg, result)

    def test_prepare_message_with_data(self):
        data = {
            'event': 'node-test',
            'parameters': {
                0: 'abcd'
            },
            'targets': ['node-lcd-40x4']
        }

        msg = self.msg.prepare_message(data)
        result = {
            'protocol': 'iot:1',
            'node': self.msg._node,
            'chip_id': self.msg._chip_id,
            'event': 'node-test',
            'parameters': {
                0: 'abcd'
            },
            'response': '',
            'targets': [
                'node-lcd-40x4'
            ]
        }

        assert_equal(msg, result)

    def test_decode_message(self):
        self.msg._chip_id = 'a'
        result = {
            'protocol': 'iot:1',
            'node': self.msg._node,
            'chip_id': self.msg._chip_id,
            'event': 'node-test',
            'parameters': {
                '0': 'abcd'
            },
            'targets': [
                'test-node'
            ]
        }
        json = '{ "protocol": "iot:1", "node": "' + self.msg._node + '", "chip_id": "' + self.msg._chip_id + '", "event": "node-test", "parameters": {"0": "abcd"}, "targets": ["test-node"]}'
        msg = self.msg.decode_message(json)
        assert_equal(msg, result)

    def test_decode_message_should_fail_wrong_protocol(self):
        result = None
        json = '{ "protocol": "iot:7", "node": "' + self.msg._node + '", "chip_id": "' + self.msg._chip_id + '", "event": "node-test", "parameters": {"0": "abcd"}, "targets": ["node-lcd-40x4"]}'
        msg = self.msg.decode_message(json)
        assert_equal(msg, result)

    def test_decode_message_should_fail_not_a_target(self):
        msg = {
            'protocol': 'iot:1',
            'node': self.msg._node,
            'chip_id': self.msg._chip_id,
            'event': 'node-test',
            'parameters': {},
            'response': '',
            'targets': [
                'node'
            ]
        }

        msg = self.msg.decode_message(json.dumps(msg))
        assert_equal(msg, None)

    def test_decode_message_should_decode_all__target(self):
        msg = {
            'protocol': 'iot:1',
            'node': self.msg._node,
            'chip_id': self.msg._chip_id,
            'event': 'node-test',
            'parameters': {},
            'targets': [
                'ALL'
            ]
        }

        msg = self.msg.decode_message(json.dumps(msg))
        assert_not_equal(msg, None)