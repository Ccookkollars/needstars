import re

import numpy as np


def parse_board(text):
    seq, directions = text.split('\n\n')
    directions = [re.findall('[A-Z0-9]{3}', d) for d in directions.split('\n')]
    directions = {k: (l, r) for k, l, r in directions}
    return seq, directions


def perform(seq, directions):
    i = 0
    step = 'AAA'
    while True:
        if step == 'ZZZ':
            return i
        for c in seq:
            i += 1
            print(step)
            if step == 'ZZZ':
                return i

            step = directions[step][0 if c == 'L' else 1]


def perform2(seq, directions):
    n_steps = 0
    steps = tuple(d for d in directions if d.endswith('A'))
    hits = tuple([] for _ in steps)

    for _ in range(1000):
        for c in seq:
            n_steps += 1
            for snum, s in enumerate(steps):
                if s.endswith('Z'):
                    hits[snum].append(n_steps)
                    print(hits)
            nexts = tuple(directions[s][0 if c == 'L' else 1] for s in steps)
            steps = nexts

    return np.lcm.reduce([round(np.polyfit(range(len(ys)), ys, 1)[0]) for ys in hits])


with open('08_01.txt', 'r') as infile:
    text = infile.read()

seq, directions = parse_board(text)
# print(perform(seq, directions))
print(perform2(seq, directions))
