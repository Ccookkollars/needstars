import functools

import numpy as np
from tqdm import tqdm

all_directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]


def print_board(dat=None, x=None, y=None, states=None):
    print('=====')
    if states is None:
        states = []
    if dat is None:
        dat = board

    def get_xline(x, y):
        line = ''.join([c if (localx, y) not in states else 'O' for localx, c in enumerate(dat[y])])
        return line if x is None else line[x - 8:x + 8]

    for y in range(len(dat)) if y is None else range(y - 8, y + 8):
        print(''.join(get_xline(x, y)))
    print('=====')


position_of_start = None


def yield_lines(filename):
    global position_of_start
    with open(filename, 'r') as infile:
        for i, line in enumerate(infile.read().split('\n')):
            if 'S' in line:
                position_of_start = (line.find('S'), i)
            yield line


def modify_state(state, vec):
    return state[0] + vec[0], state[1] + vec[1]


def is_valid(state, board):
    if state[0] < 0 or state[0] >= len(board[0]):
        return False
    if state[1] < 0 or state[1] >= len(board):
        return False
    return board[state[1]][state[0]] != '#'


@functools.cache
def get_next_steps(state):
    result = [modify_state(state, d) for d in all_directions]
    return [r for r in result if is_valid(r, board)]


def get_start_pos():
    for y in range(len(board)):
        pos = board[y].find('S')
        if pos > 0:
            return pos, y


def op(nsteps):
    results = []
    states = {get_start_pos()}
    for i in tqdm(range(nsteps)):
        prev_nstates = len(states)
        next_states = set()
        for state in states:
            next_states.update(get_next_steps(state))
        states = next_states
        nstates = len(states)
        results.append((i, nstates, prev_nstates))

        # print_board(states=states)
    print('i\tstates\tprevstates')
    for r in results:
        print('\t'.join([str(s) for s in r]))
    return len(states)


def embiggen(board, n=100):
    result = []

    def add_row(is_middle=False):
        for i, line in enumerate(board):
            nline = line.replace('S', '.')
            row = ''
            for x in range(int(n / 2)):
                row += nline
            row += (line if is_middle and i == ((len(board) - 1) / 2) else nline)
            for x in range(int(n / 2)):
                row += nline
            result.append(row)

    for y in range(int(n / 2)):
        add_row()
    add_row(is_middle=True)
    for y in range(int(n / 2)):
        add_row()
    return result


def op2():
    a1 = np.array(
        [3, 5, 7, 9, 10, 13, 11, 18, 10, 23, 21, 25, 25, 26, 27, 30, 31, 37, 33, 42, 35, 46, 34, 54, 30, 58, 39, 64, 43,
         68, 45, 65, 50, 67, 54, 76, 47, 84, 57, 90, 58, 89, 68, 88, 73, 89, 85, 90, 86, 87, 97, 94, 92, 95, 97, 90,
         106, 104, 111, 107, 117, 131, 125, 138, 125, 139, 129, 143, 105, 138, 116, 150, 114, 154, 122, 160, 116, 162,
         121, 179, 123, 184, 115, 191, 115, 192, 123, 200, 132, 189, 141, 181, 147, 188, 150, 198, 157, 197, 164, 187,
         183, 185, 185, 189, 188, 187, 198, 200, 191, 202, 214, 188, 218, 187, 217, 203, 222, 210, 214, 214, 226, 222,
         218, 227, 229, 232, 221, 235, 237, 247, 239])
    a2 = np.array(
        [236, 240, 236, 238, 239, 241, 223, 244, 236, 240, 235, 229, 243, 234, 242, 221, 253, 223, 245, 244, 228, 242,
         230, 241, 218, 249, 224, 247, 221, 257, 216, 257, 205, 263, 211, 259, 198, 264, 203, 268, 193, 287, 202, 276,
         193, 283, 198, 276, 205, 266, 220, 264, 202, 254, 214, 251, 214, 259, 224, 250, 224, 274, 251, 282, 250, 274,
         250, 274, 222, 246, 225, 251, 221, 246, 220, 252, 210, 256, 220, 269, 209, 272, 200, 281, 190, 279, 189, 288,
         190, 279, 194, 269, 192, 266, 199, 272, 203, 266, 208, 254, 225, 252, 224, 251, 216, 241, 229, 248, 227, 246,
         247, 224, 250, 217, 244, 229, 247, 235, 234, 237, 237, 240, 227, 242, 239, 241, 228, 240, 240, 248, 238])
    n = 130
    v = 15805
    multiplier = 1
    while True:
        for pos in range(len(a1)):
            if n == 26501364 - 1:
                print(n, v)
                return
            v += a1[pos]
            v += (a2[pos] * multiplier)
            n += 1
        multiplier += 1


# print_board(embiggen(['1.2', '3S4', '5.6'], n=3))

board = list(yield_lines('21_01.txt'))
board = embiggen(board, n=100)

# op(10)
op2()
