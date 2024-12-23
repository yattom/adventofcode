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


def secret_number(seed):
    step1 = ((seed * 64) ^ seed) % 16777216
    step2 = (int(step1 / 32) ^ step1) % 16777216
    step3 = ((step2 * 2048) ^ step2) % 16777216

    return step3


def puzzle1(lines: list[str]):
    total = 0
    for seed in [int(l) for l in lines]:
        n = seed
        for i in range(2000):
            n = secret_number(n)
        total += n
    return total


def puzzle2(lines: list[str]):
    buyer_numbers = []
    for seed in [int(l) for l in lines]:
        n = seed
        numbers = [n]
        for i in range(2000):
            n = secret_number(n)
            numbers.append(n)
        buyer_numbers.append(numbers)

    buyer_prices = [[int(str(n)[-1]) for n in numbers] for numbers in buyer_numbers]
    buyer_changes = []
    for prices in buyer_prices:
        changes = []
        for i, p in enumerate(prices):
            if i == 0:
                changes.append(None)
                continue
            changes.append(prices[i] - prices[i - 1])
        buyer_changes.append(changes)

    sequences = dict()
    for b, changes in enumerate(buyer_changes):
        appeared_sequences_for_buyer = set()
        for i in range(4, len(changes)):
            seq = tuple(changes[i - 3: i + 1])
            if seq in appeared_sequences_for_buyer:
                continue
            appeared_sequences_for_buyer.add(seq)
            if seq not in sequences:
                sequences[seq] = 0
            sequences[seq] += buyer_prices[b][i]

    max_value = max(sequences.values())
    return max_value


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
