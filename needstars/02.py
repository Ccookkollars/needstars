import os
import re
from collections import defaultdict


def parse_line(line):
    game, content = line.split(':')
    game_number = int(re.findall(r'\d+', game)[0])
    rounds = content.split(';')

    colors = defaultdict(lambda: 0)
    for i, round in enumerate(rounds):
        for sampling in round.strip().split(','):
            color = re.findall(r'[a-z]+', sampling)[0]
            number = int(re.findall(r'\d+', sampling)[0])

            colors[color] = max(colors[color], number)
    print(f'game {game_number} colors: {dict(colors)}')

    return game_number, colors


def part1_proc(lines):
    for line in lines:
        game_number, colors = parse_line(line)

        possible = True
        for color in colors:
            if colors[color] > maxcolors[color]:
                possible = False

        if possible:
            print(f'>{game_number} is possible')
            yield game_number


def part2_proc(lines):
    for line in lines:
        game_number, colors = parse_line(line)

        power = colors['red'] * colors['green'] * colors['blue']

        yield power


def play_game(filepath, maxcolors, proc_lines):
    with open(filepath, 'r') as infile:
        lines = infile.read().split(os.linesep)

    print(sum(proc_lines(lines)))


maxcolors = {'blue': 14, 'green': 13, 'red': 12}
play_game('02_01.txt', maxcolors, part2_proc)
