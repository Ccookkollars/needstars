import os
import re


def parse_board(text):
    lines = [[int(i) for i in re.findall(r'-?\d+', line)] for line in text.split(os.linesep)]
    return lines



def make_stack(line):
    print(f'line{line}')
    dat = line
    stack = [dat]
    while True:

        diffs = [y - x for x, y in zip(dat[:-1], dat[1:])]
        dat = diffs
        stack.append(diffs)

        if all(d == 0 for d in diffs):
            break

    for s in stack:
        print(f'deltad {s}')
    return stack


def part1(stack):
    stack[-1].append(0)
    for i in reversed(range(len(stack) - 1)):
        stack[i].append(stack[i][-1] + stack[i + 1][-1])

    return stack[0][-1]


def part2(stack):
    stack[-1].insert(0, 0)
    for i in reversed(range(len(stack) - 1)):


        stack[i].insert(0, stack[i][0] - stack[i + 1][0])

    return stack[0][0]


with open('09_01.txt', 'r') as infile:
    text = infile.read()
lines = parse_board(text)

print(sum(part2(make_stack(line)) for line in lines))
