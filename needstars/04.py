import os
import re
from collections import defaultdict

starmap = defaultdict(list)


def get_card(line):
    cardseg, segs = line.split(':')
    startseg, endseg = segs.split('|')
    cardnum = int(re.search(r'(\d+)+', cardseg)[0])
    startnums = [int(s) for s in re.findall(r'(\d+)+', startseg)]
    endnums = [int(s) for s in re.findall(r'(\d+)+', endseg)]
    return cardnum, startnums, endnums


def get_line_points(line):
    cardnum, startnums, endnums = get_card(line)
    return get_card_points(startnums, endnums)


def get_card_points(startnums, endnums):
    nlen = len(set(startnums).intersection(set(endnums)))
    return 2 ** (nlen - 1) if nlen > 0 else 0


def do_puzzle(filepath):
    with open(filepath, 'r') as infile:
        lines = infile.read().split(os.linesep)

    return sum(
        get_line_points(line) for line in lines)


def do_part2(filepath):
    with open(filepath, 'r') as infile:
        lines = infile.read().split(os.linesep)

    cards = [get_card(line) for line in lines]

    winlist = defaultdict(lambda: 1)
    for cardnum, startnums, endnums in cards:
        n_intersect = len(set(startnums).intersection(set(endnums)))
        n_copies = winlist[cardnum]
        for card_won in range(cardnum+1, cardnum+n_intersect+1):
            winlist[card_won] += n_copies

        # print(cardnum, dict(winlist))
    print(sum(winlist.values()))


# do_puzzle('04_01.txt')
# do_part2('04_test.txt')
do_part2('04_01.txt')
