#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Advent of code 2021 day 16 - https://adventofcode.com/2021/day/16

"""Goals:
1) What do you get if you add up the version numbers in all packets?
2) What do you get if you evaluate the expression represented by your hexadecimal-encoded BITS
transmission?
"""

# Programmed by CoolCat467

__title__ = 'Advent of Code 2021 - Day 16'
__author__ = 'CoolCat467'
__version__ = '0.0.0'
__ver_major__ = 0
__ver_minor__ = 0
__ver_patch__ = 0

from functools import reduce

class Connection:
    "Base connection class."
    def __init__(self):
        """Initialize self.send and self.received to an empty bytearray."""
        self.sent = []
        self.received = []
        self.read_bits = 0
    
    def __repr__(self):
        return f'{self.__class__.__name__} Object'
    
    def read(self, length):
        """Return self.recieved up to length bytes, then cut recieved up to that point."""
        result = self.received[:length]
        self.read_bits += length
        self.received = self.received[length:]
        return result
    
    def write(self, data):
        """Extend self.sent from data."""
        if isinstance(data, Connection):
            data = data.flush()
        if isinstance(data, str):
            data = list(data)
        self.sent.extend(data)
    
    def receive(self, data):
        """Extend self.received with data."""
        if not isinstance(data, list):
            data = list(data)
        self.received.extend(data)
    
    def remaining(self):
        """Return length of self.received."""
        return len(self.received)
    
    def flush(self):
        """Return self.sent. Clears self.sent."""
        result = self.sent
        self.sent = []
        return result
    
    def read_bit(self):
        "Return 1 or 0, read from one bit."
        return int(''.join(self.read(1)))
    
    def read_int(self, length):
        "Return length bits read as int from binary"
        if length == -1:
            length = self.remaining()
        return int(''.join(self.read(length)), 2)

def eval_operator(values, op_type):
    "Evaluate operator"
    if len(values) == 1:
        return values[0]
    if op_type == 0:#Sum packet
        return sum(values)
    if op_type == 1:#Product packet
        return reduce(lambda x,y:x*y, values)
    if op_type == 2:#Minimum packet
        return min(values)
    if op_type == 3:#Maximum packet
        return max(values)
    # 4 is literal
    if op_type == 5:#Greater than packet
        return int(values[0] > values[1])
    if op_type == 6:#Less than packet
        return int(values[0] < values[1])
    if op_type == 7:#Equal to packet
        return int(values[0] == values[1])
    print(f'Invalid op_type {op_type}')
    return values

def read_literal(connection, version):
    "Read literal number"
    buffer = Connection()
    cont = 1
    while cont:
        cont = connection.read_bit()
        buffer.receive(connection.read(4))
    return buffer.read_int(-1)

def read_operator(connection, type_id, version):
    "Read operator"
    length_type_id = connection.read_bit()
    if not length_type_id:#type 0
        length = connection.read_int(15)
    else:#type 1
        length = connection.read_int(11)
    vers_sum = 0
    if not length_type_id:#type 0
        buffer = Connection()
        buffer.receive(connection.read(length))
        data = []
        while buffer.remaining():
            packet, version = read_packet(buffer)
            data.append(packet)
            vers_sum += version
    else:#type 1
        data = []
        for _ in range(length):
            packet, version = read_packet(connection)
            data.append(packet)
            vers_sum += version
    value = eval_operator(data, type_id)
    return value, vers_sum

def read_packet(connection):
    "Read packet"
    if connection.remaining() < 6+5:
        hex_fix = 4 - (connection.read_bits % 4)
        connection.read(hex_fix)
        return None, 0
    version = connection.read_int(3)
    type_id = connection.read_int(3)
    if type_id == 4:
        # literal value
        value = read_literal(connection, version)
    else:
        # operator
        value, vers_add = read_operator(connection, type_id, version)
        version += vers_add
    return value, version

def run():
    "Solve problems"
    # Read file
    data = []
    with open('adv16.txt', 'r', encoding='utf-8') as rfile:
        data = rfile.read().strip()
        rfile.close()
    # Process data
    bits = ''.join(f'{int(x,16):>04b}' for x in data)
    buffer = Connection()
    buffer.receive(bits)
    
    # Solve 1
    version_sum = 0
    packets = []
    while buffer.remaining():
        packet, vers_sum = read_packet(buffer)
        if not packet is None:
            packets.append(packet)
            version_sum += vers_sum
    print(version_sum)
    
    # Solve 2
    print(packets[0])

if __name__ == '__main__':
    print(f'{__title__} v{__version__}\nProgrammed by {__author__}.')
    run()
