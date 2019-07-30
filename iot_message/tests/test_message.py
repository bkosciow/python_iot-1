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


class TestMessage(object):
    def setUp(self):
        message.Message.chip_id = 'miau'

    def test_init_with_chip_id(self):
        msg = message.Message()
        assert_equal(msg.chip_id, 'miau')

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

    def test_encode_message(self):
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

        assert_equal(bytes(msg), json.dumps(data).encode())
