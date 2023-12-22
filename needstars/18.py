import itertools

import shapely
from matplotlib import pyplot as plt

size = 1000
board = [['.' for i in range(size)] for j in range(size)]

heading_map = {'R': (1, 0), 'L': (-1, 0), 'U': (0, -1), 'D': (0, 1)}
num_to_direction = {'0': 'R', '1': 'D', '2': 'L', '3': 'U'}

all_directions = set(itertools.product((-1, 0, 1), (-1, 0, 1)))
all_directions.remove((0, 0))

PART2 = False

if PART2:
    def read_line(line):
        heading, num, color = line.split(' ')
        # return heading, int(num)
        return num_to_direction[color[7]], int(color[2:7], 16)
else:
    def read_line(line):
        heading, num, color = line.split(' ')
        return heading, int(num)


def run_line(line, state):
    state = state[:2] + heading_map[line[0]]
    for i in range(line[1]):
        next_pos = (state[0] + state[2], state[1] + state[3]) + state[2:]
        # print(state, next_pos)
        board[state[1]][state[0]] = '#'
        state = next_pos  # print_board()
    return next_pos


def get_score():
    seen = set()
    to_visit = [(int(size / 2 + 1), int(size / 2) + 1)]
    while to_visit:
        item = to_visit.pop()
        seen.add(item)
        board[item[1]][item[0]] = '*'
        for d in all_directions:
            next_item = item[0] + d[0], item[1] + d[1]
            if next_item in seen or board[next_item[1]][next_item[0]] == '#':
                continue
            to_visit.append(next_item)  # print_board(*item)  # print_board()

    return len(seen) + sum([line.count('#') for line in board])


def yield_lines(filename):
    with open(filename, 'r') as infile:
        for line in infile.read().split('\n'):
            yield line


def prep(lines):
    state = (int(size / 2), int(size / 2), 1, 0)
    for line in lines:
        state = run_line(read_line(line), state)


def get_polygon(lines):
    x = y = 0
    points = []
    for direction, duration in [read_line(l) for l in lines]:
        x += heading_map[direction][0] * duration
        y += heading_map[direction][1] * duration
        points.append((x, y))
    return shapely.Polygon(points)


filename = '18_01.txt'
if PART2:
    pgon = get_polygon(yield_lines(filename))

    x, y = pgon.exterior.xy
    plt.plot(x, y)
    plt.show()
    print(pgon.area + pgon.length / 2 + 1)
else:
    prep(yield_lines(filename))
    print(get_score())
