#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Advent of Code 2022 Day 16

"Advent of Code 2022 Day 16"

# Programmed by CoolCat467

__title__ = 'Advent of Code 2022 Day 16'
__author__ = 'CoolCat467'
__version__ = '0.0.0'


##from typing import Iterator, Iterable, cast

import io


def get_gained(time_left: int,
               current: str,
               connections: dict[str, tuple[str, ...]],
               flow_rates: dict[str, tuple[str, ...]],
               valves_open: set[str]) -> dict[str, int]:
    def handle_node(cur: str, minute: int, prev_visited: set[str]) -> dict:
        visited = prev_visited | {cur}
        gained = {}
        for valve in connections[cur] + (cur,):
            if valve in valves_open:
                gained[valve] = 0
            elif valve in connections[cur]:
                gained[valve] = flow_rates[valve] * (minute - 2)
            else:
                gained[valve] = flow_rates[valve] * (minute - 1)
            if valve not in visited:
                for v, gain in handle_node(valve, minute - 1, visited).items():
                    if v not in gained:
                        gained[v] = 0
                    gained[v] += gain
##                    gained[valve] += gain // 4
        return gained
    gained = handle_node(current, time_left, set())
    print(f'{gained = }')
    return gained


def part_one(valves: dict[str, tuple[int, tuple[str, ...]]]) -> int:
    flow_rates = {name:data[0] for name, data in valves.items()}
    connections = {name:data[1] for name, data in valves.items()}
    current = 'AA'
    valves_open: set[str] = set()
    minutes = 30
    released = 0
    while minutes > 0:
        released += sum(flow_rates[v] for v in valves_open)
        gained = get_gained(minutes, current,
                            connections, flow_rates, valves_open)
##        print(f'{gained = }')
        travel = {v:k for k,v in gained.items() if k in connections[current] or k == current}
        last = current
        while True:
            if not travel:
                if current != last:
                    print(f'{31-minutes}: Traveled to {last}\n')
                    current = last
                break
            max_val = max(travel)
            new = travel[max_val]
            print(f'{travel = }')
            if not current in valves_open:
                if new == current:
                    print(f'{31-minutes}: Opened valve {current}\n')
                    valves_open.add(current)
                    break
                elif flow_rates[current] * (minutes - 1) > flow_rates[new] * (minutes - 1):
                    print(f'{31-minutes}: Opened valve {current}\n')
                    valves_open.add(current)
                    break
                else:
                    print(f'{31-minutes}: Traveled to {new}\n')
                    current = new
                    break
            if current != new:
                print(f'{31-minutes}: Traveled to {new}\n')
                current = new
                break
            last = new
            del travel[max_val]
        minutes -= 1
    return released


def part_two(valves: dict[str, tuple[int, tuple[str, ...]]]) -> int:
    ...


def run() -> None:
    "Synchronous entry point"
    test_data = """Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II"""

    file = io.StringIO(test_data)
##    file = open('day16.txt', encoding='utf-8')

    valves: dict[str, tuple[int, tuple[str, ...]]] = {}

    for line in file:
        name_rate, tunnels = line.split(';', 1)
        parts = name_rate.split(' ')
        name = parts[1]
        rate = int(parts[4].removeprefix('rate='))
        tunnels = tunnels.split('valve')[1].removeprefix('s').strip()
        connections = tunnels.split(', ')
        valves[name] = (rate, tuple(connections))

    file.close()

    print(f'{part_one(valves) = }')
    print(f'{part_two(valves) = }')


if __name__ == '__main__':
    print(f'{__title__}\nProgrammed by {__author__}.\n')
    run()
