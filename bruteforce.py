def make(n):
    rows = 2**n
    ones = (1 << rows) - 1

    def var(x):
        out = 0
        for i in range(rows):
            out |=  ((i // (2**x) + 1) & 1) << i
        return out

    def _not(a):
        return ones - a

    def _and(a, b):
        return a & b

    def _or(a, b):
        return a | b

    def v2s(x):
        return bin(x)[2:].rjust(rows, '0')

    return var, _not, _and, _or, v2s

def find_bruteforce(n, signals, gates, goals, cb, stack=[]):
    if (n <= 0):
        if n == 0 and all([goal in signals for goal in goals]):
            cb(signals, stack)
        return

    for i in range(len(signals)):
        for j in range(len(signals)):
            for k in range(len(gates)):
                gate, cost = gates[k]
                out = gate(signals[i], signals[j])
                if (out in signals): continue

                find_bruteforce(
                    n - cost,
                    signals + [out],
                    gates,
                    goals,
                    cb,
                    stack + [[i, j, k]]
                )

