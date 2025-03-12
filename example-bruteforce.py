#!/bin/env python3

from bruteforce import make, find_bruteforce

def nand(a, b): return _not(_and(a, b))

var, _not, _and, _or, v2s = make(2)
a = var(0)
b = var(1)
eq = 0b1001
gt = 0b0100
lt = 0b0010

signals = [a, b]
gates = [[nand, 1]]
goals = [eq, gt, lt]

def cb(signals, stack):
    print([v2s(sig) for sig in signals])
    print(stack)
    print()
    exit()

find_bruteforce(7, signals, gates, goals, cb)
