import math
import re

import numpy as np


def parse_board(text):
    remainder, distnumtext = text.split('Distance:')
    distances = [int(i) for i in re.findall(r'\d+', distnumtext)]
    times = [int(i) for i in re.findall(r'\d+', remainder)]

    return dict(distances=distances, times=times)


def get_score(time, distance):
    # 0 = i*time - i**2 - distance
    roots = sorted(np.roots((-1, time, -distance - 0.0001)))
    return math.ceil(roots[1]) - math.ceil(roots[0])


def do_puzzle(filepath):
    with open(filepath, 'r') as infile:
        text = infile.read()

    board = parse_board(text)

    result = 1

    for distance, time in zip(board['distances'], board['times']):
        result *= get_score(time, distance)
    return result


def do_puzzle2(filepath):
    with open(filepath, 'r') as infile:
        text = infile.read()

    remainder, distnumtext = text.split('Distance:')
    distance = int(re.findall(r'\d+', distnumtext.replace(' ', ''))[0])
    time = int(re.findall(r'\d+', remainder.replace(' ', ''))[0])

    return get_score(time, distance)


print(do_puzzle2('06_01.txt'))
