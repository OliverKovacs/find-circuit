from z3 import *

def id(a):
    return a

def _not(a):
    return ~a

def _and(a, b):
    return a & b

def _or(a, b):
    return a | b

def wire(srcs, dest, conn):
    return [conn(dest, e) for e in enumerate(srcs)]

def map_name(v1, v2, post):
    return str(v1)[0] + '->' + str(v2) + post

def map_constraint(src, dest, post):
    idx, sig = src
    return Int(map_name(sig, dest, post)) == idx

def equal_map(transform, post = ""):
    return lambda dest, src: And(
        dest == transform(src[1]),
        map_constraint(src, dest, post),
    )

def wire_gate(srcs, dest, gate):
    return wire(srcs, dest, lambda _, src: And(
        map_constraint(src, dest, "[0]"),
        Or(wire(srcs, dest, equal_map(gate(src[1]), "[1]"))),
    ))

def constrain(_vars, consts):
    return And([a == b for a, b in zip(_vars, consts)])

def find_z3(n, signal_constants, gate, goal_constants, B):
    k = len(signal_constants)
    signal_vars = [BitVec('s_' + str(i), B) for i in range(k + n + 1)]
    signal_constraints = constrain(signal_vars[:k], signal_constants)

    gate_wires = []
    for i in range(k, k + n + 1):
        gate_wires.append(Or(wire_gate(signal_vars[0:i], signal_vars[i], gate)))
    gate_wires = And(gate_wires)

    goal_vars = [BitVec('o_' + str(i), B) for i in range(len(goal_constants))]
    goal_constraints = constrain(goal_vars, goal_constants)
    goal_wires = And([Or(wire(signal_vars, goal, equal_map(id))) for goal in goal_vars])

    s = Solver()
    s.add(And(signal_constraints, gate_wires, goal_wires, goal_constraints))
    s.check()
    return s
