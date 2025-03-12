#!/bin/env python3

from z3 import BitVecVal
from solver import find_z3, _not, _and

def nand(a):
    return lambda b: _not(_and(a, b))

B = 2**2

a = BitVecVal(0b0011, B)
b = BitVecVal(0b0101, B)

lt = BitVecVal(0b0100, B)
gt = BitVecVal(0b0010, B)
eq = BitVecVal(0b1001, B)

signals = [a, b]
goals = [lt, gt, eq]
gate = nand

s = find_z3(7, signals, gate, goals, B)
print(s.model())
