import copy
import dataclasses
import re

from tqdm import tqdm


@dataclasses.dataclass
class Board:
    dat: list
    energized: list


def parse_board(filename):
    with open(filename, 'r') as infile:
        text = infile.read()
    dat = [[c for c in line] for line in text.split('\n')]
    return Board(dat=dat, energized=[['.' for _ in line] for line in dat])


def print_board(board):
    print('=====')
    dat = board.dat
    for y in range(len(dat)):
        print(''.join(dat[y]))
    print('===energy===')
    energized = board.energized
    for y in range(len(energized)):
        print(''.join(map(str, energized[y])))
    print('=====')


def get_next_pos(x, y, heading):
    if heading == 0:
        return x + 1, y, heading
    elif heading == 1:
        return x, y - 1, heading
    elif heading == 2:
        return x - 1, y, heading
    else:
        return x, y + 1, heading


def get_energy_level(energy, heading):
    if energy == '.':
        energy = '0000'
    else:
        energy = bin(int(energy, 16))[2:].zfill(4)
    energy = energy[:3 - heading] + '1' + energy[4 - heading:]
    return hex(int(energy, 2))[2:]


def propagate(board, x, y, heading):
    if not 0 <= y < len(board.dat):
        return []
    if not 0 <= x < len(board.dat[0]):
        return []
    energy_level = get_energy_level(board.energized[y][x], heading)
    if energy_level == board.energized[y][x]:
        return []

    c = board.dat[y][x]
    to_prop = []
    board.energized[y][x] = energy_level

    if c == '.':
        next_pos = get_next_pos(x, y, heading)
        to_prop.append(next_pos)
    elif c == '/':
        if heading == 0:
            to_prop.append(get_next_pos(x, y, 1))
        elif heading == 1:
            to_prop.append(get_next_pos(x, y, 0))
        elif heading == 2:
            to_prop.append(get_next_pos(x, y, 3))
        elif heading == 3:
            to_prop.append(get_next_pos(x, y, 2))
    elif c == '\\':
        if heading == 0:
            to_prop.append(get_next_pos(x, y, 3))
        elif heading == 3:
            to_prop.append(get_next_pos(x, y, 0))
        elif heading == 2:
            to_prop.append(get_next_pos(x, y, 1))
        elif heading == 1:
            to_prop.append(get_next_pos(x, y, 2))
    elif c == '|':
        if heading in {0, 2}:
            to_prop.append(get_next_pos(x, y, 1))
            to_prop.append(get_next_pos(x, y, 3))
        else:
            to_prop.append(get_next_pos(x, y, heading))
    elif c == '-':
        if heading in {1, 3}:
            to_prop.append(get_next_pos(x, y, 0))
            to_prop.append(get_next_pos(x, y, 2))
        else:
            to_prop.append(get_next_pos(x, y, heading))
    # print(f'Done propagating {x, y, heading}')
    # print_board(board)
    return to_prop


def count_score(board):
    return sum([len(list(re.finditer(r'[0-9a-f]', ''.join(map(str, e))))) for e in board.energized])


def get_score(board, x=0, y=0, heading=0):
    board = Board(**copy.deepcopy(dataclasses.asdict(board)))
    to_prop = propagate(board, x, y, heading)
    while to_prop:
        to_prop.extend(propagate(board, *to_prop.pop()))
    return count_score(board), board


def get_score_allways(board):
    to_test = []
    score = 0
    for x in range(len(board.dat)):
        to_test.append((x, 0, 3))
        to_test.append((x, len(board.dat[0]), 1))
    for y in range(len(board.dat[0])):
        to_test.append((0, y, 0))
        to_test.append((len(board.dat), y, 2))

    for initial in tqdm(to_test):
        this_score, this_board = get_score(board, *initial)
        if this_score > score:
            score = this_score
            print_board(this_board)
            print(f'New top score {score}')
    return score


board = parse_board('16_01.txt')
print(get_score_allways(board))
