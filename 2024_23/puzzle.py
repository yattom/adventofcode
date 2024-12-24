import re
import time
from copy import copy
from dataclasses import dataclass
from typing import TypeAlias


class DebugPrinter:
    def __init__(self, enabled=False, interval=0):
        self.enabled = enabled
        self.interval = interval
        if self.interval:
            self.start_ns = time.time_ns()
            self.last_ns = self.start_ns

    def print(self, *args, **kwargs):
        if self.enabled:
            print(*args, **kwargs)

    def at_interval(self) -> bool:
        if not self.enabled or not self.interval:
            return False
        if time.time_ns() - self.last_ns > self.interval:
            self.last_ns += self.interval
            return True

    def elapsed(self):
        return (time.time_ns() - self.start_ns) / (1000 * 1000 * 1000)


def memoize(func):
    memo = {}

    def wrapper(*args, **kwargs):
        key = (repr(args), repr(kwargs.items()))
        if key not in memo:
            memo[key] = func(*args, **kwargs)
        return copy(memo[key])

    return wrapper


dp = DebugPrinter(enabled=False)


def puzzle1(lines: list[str]):
    pairs = set()
    nodes = set()
    network_id = 0
    network = dict()
    for l in lines:
        n1, n2 = l.strip().split('-')
        pairs.add((n1, n2))
        nodes.add(n1)
        nodes.add(n2)

    connected_nodes = dict()
    for node in nodes:
        connected = set()
        for pair in pairs:
            if pair[0] == node:
                connected.add(pair[1])
            elif pair[1] == node:
                connected.add(pair[0])
        connected_nodes[node] = connected

    three_combinations = set()
    for node in nodes:
        connected = connected_nodes[node]
        for c in connected:
            mutually_connected = connected & connected_nodes[c]
            for mc in mutually_connected:
                three_combinations.add(tuple(sorted([node, c, mc])))

    suspected_combinations = set()
    for combination in three_combinations:
        if any([n.startswith('t') for n in combination]):
            suspected_combinations.add(combination)
    print(three_combinations)
    print(suspected_combinations)
    return len(suspected_combinations)


def puzzle2(lines: list[str]):
    pairs = set()
    nodes = set()
    network_id = 0
    network = dict()
    for l in lines:
        n1, n2 = l.strip().split('-')
        pairs.add((n1, n2))
        nodes.add(n1)
        nodes.add(n2)

    connected_nodes = dict()
    for node in nodes:
        connected = set()
        for pair in pairs:
            if pair[0] == node:
                connected.add(pair[1])
            elif pair[1] == node:
                connected.add(pair[0])
        connected_nodes[node] = connected

    clusters = []
    for node in nodes:
        for cluster in clusters:
            if node not in cluster and cluster <= connected_nodes[node]:
                cluster.add(node)
        else:
            clusters.append({node})

    max_size = max([len(c) for c in clusters])
    largest_cluster = [c for c in clusters if len(c) == max_size][0]
    return ','.join(sorted(largest_cluster))


def main():
    import sys
    if len(sys.argv) == 1:
        lines = sys.stdin.readlines()
    else:
        with open(sys.argv[1]) as f:
            lines = f.readlines()
    print(puzzle1(lines))
    print(puzzle2(lines))


if __name__ == "__main__":
    main()
