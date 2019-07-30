#!/usr/bin/python3
import os
import subprocess
import json

__author__ = 'Bartosz Kościów'


class Message(object):
    """Class Message"""
    protocol = "iot:1"
    chip_id = None
    node_name = None

    def __init__(self):
        if self.chip_id is None:
            self.chip_id = self._get_id()

        if self.node_name is None:
            self.node_name = self._get_node_name()

        self.data = None

    def _get_id(self):
        """:return string"""
        if 'nt' in os.name:
            return subprocess.getoutput('wmic csproduct get uuid')
        else:
            return subprocess.getoutput('cat /var/lib/dbus/machine-id')

    def _get_node_name(self):
        import socket
        return socket.gethostname()

    def _initialize_data(self):
        self.data = {
            'protocol': self.protocol,
            'node': self.node_name,
            'chip_id': self.chip_id,
            'event': '',
            'parameters': {},
            'response': '',
            'targets': [
                'ALL'
            ]
        }

    def set(self, data):
        if self.data is None:
            self._initialize_data()

        for k, v in data.items():
            self.data[k] = v

    def __bytes__(self):
        return json.dumps(self.data).encode()

    def __repr__(self):
        return json.dumps(self.data)