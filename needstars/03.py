import os
import re
from collections import defaultdict

import math

starmap = defaultdict(list)


def yield_positions(xstart, xstop, ypos, xbound, ybound):
    points = []
    points.append((xstart - 1, ypos))
    points.extend((x, ypos + 1) for x in range(xstart - 1, xstop + 1))
    points.append((xstop, ypos))
    points.extend(reversed(list((x, ypos - 1) for x in range(xstart - 1, xstop + 1))))

    return [(x, y)
            for x, y in points
            if x >= xbound[0]
            and x < xbound[1]
            and y >= ybound[0]
            and y < ybound[1]]


def get_stars_for_num(board, match, y):
    stars = set()
    seen_mark = False
    for p in yield_positions(match.start(), match.end(), y,
                             (0, len(board[0])),
                             (0, len(board))):
        c = board[p[1]][p[0]]
        if c.isnumeric() or c == '.':
            continue
        seen_mark = True
        if c == '*':
            stars.add(p)
    return list(stars) if seen_mark else None


def do_puzzle(filepath):
    with open(filepath, 'r') as infile:

        lines = infile.read().split(os.linesep)
        board = [[c for c in line] for line in lines]

    def get_nums():
        for y, line in enumerate(lines):
            numbers = re.finditer(r'\d+', line)
            for number in numbers:
                stars = get_stars_for_num(board, number, y)
                if stars is None:
                    continue
                for star in stars:
                    starmap[star].append(int(number.group()))
                yield int(number.group())

    print(f'part 1: {sum(get_nums())}')

    [print(star, nums, math.prod(nums)) for star, nums in starmap.items() if len(nums) > 1]
    print(f'part 2: {sum(math.prod(nums) for star, nums in starmap.items() if len(nums) > 1)}')


do_puzzle('03_01.txt')
