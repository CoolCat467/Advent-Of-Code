#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Advent of code 2021 day 3 - https://adventofcode.com/2021/day/3

"""Goals:
1) Find power usage
2) Find life support rating
"""

# Programmed by CoolCat467

__title__ = 'Advent of Code 2021 - Day 3'
__author__ = 'CoolCat467'
__version__ = '0.0.0'
__ver_major__ = 0
__ver_minor__ = 0
__ver_patch__ = 0

def activation(value):
    "Activation function"
    if value >= 0.5:
        return 1
    return 0

def mean(values: iter):
    "Return mean of values."
    return sum(values) / len(values) 

def to_bits(value: iter):
    "Return iterable of zeros and ones as binary -> int"
    return int(''.join(map(str, value)), 2)

def bit_invert(number):
    "Invert the bits of number."
    bits = number.bit_length()
    mask = int(''.join(['1']*bits), 2)
    return number ^ mask

def get_mean(bits):
    "Return mean of bits"
    bits_per = {}
    for value in bits:
        for idx, atpos in enumerate(value):
            if not idx in bits_per:
                bits_per[idx] = []
            bits_per[idx].append(int(atpos))
    return [mean(value) for value in bits_per.values()]

def get_bit_crit(bits, mode, pos):
    "Return bit criteria"
    mean_value = get_mean(bits)[pos]
    return activation(mean_value) ^ mode

def find_rating(bits, mode):
    "Find rating"
    bits = list(bits)
    index = 0
    while len(bits) > 1:
        bit_crit = get_bit_crit(bits, mode, index)
        for idx, byte in reversed(tuple(enumerate(bits))):
            if int(byte[index]) != bit_crit:
                del bits[idx]
        index += 1
    return to_bits(bits[0])

def run():
    "Solve problems"
    # Read file
    data = []
    with open('adv3.txt', 'r', encoding='utf-8') as rfile:
        data = rfile.read().splitlines()
        rfile.close()
    # Solve 1
    mean_bits = get_mean(data)
    active = [activation(x) for x in mean_bits]
    gamma = to_bits(active)
    epsilon = bit_invert(gamma)
    print(gamma * epsilon)
    # Solve 2
    oxygen_rating = find_rating(data, 0)
    co2_rating = find_rating(data, 1)
    print(oxygen_rating * co2_rating)

if __name__ == '__main__':
    print(f'{__title__} v{__version__}\nProgrammed by {__author__}.')
    run()
