import dataclasses

from tqdm import tqdm

headers = ['seed-to-soil', 'soil-to-fertilizer', 'fertilizer-to-water', 'water-to-light', 'light-to-temperature', 'temperature-to-humidity', 'humidity-to-location']


@dataclasses.dataclass
class Ranger:
    name: str
    start: int
    stop: int
    delta: int


def parse_ranger(item, line):
    soil, seed, length = [int(i) for i in line.split(' ')]
    return Ranger(name=item, start=seed, stop=seed + length, delta=soil - seed)


def parse_board(text):
    results = {}
    front = text
    for item in reversed(headers):
        snaked = item.replace('-', '_')
        front, rest = front.split(item)
        value = rest.split(':')[1].strip().split('\n')
        results[snaked] = [parse_ranger(snaked, line) for line in value]

    # then do seeds
    front, rest = front.split('seed')
    value = rest.split(':')[1].strip().split('\n')
    results['seed'] = [int(i) for i in value[0].split(' ')]

    return results


def do_puzzle(filepath):
    with open(filepath, 'r') as infile:
        text = infile.read()
    board = parse_board(text)

    def garden(seed):
        sequence = [seed]
        value = seed
        keyname = 'seed'
        nextkey = [k for k in board if k.startswith(keyname + '_to')][0]
        nextvalue = None
        while nextkey:
            for ranger in board[nextkey]:
                if ranger.start <= value < ranger.stop:
                    nextvalue = value + ranger.delta
                    break
            if nextvalue is None:
                nextvalue = value
            keyname = nextkey.split('_')[-1]
            nextkeys = [k for k in board if k.startswith(keyname + '_to')]
            nextkey = nextkeys[0] if nextkeys else None
            value = nextvalue
            sequence.append(value)
            nextvalue = None
        return sequence

    print(min(garden(seedn)[-1] for seedn in board['seed']))


def proc_ranges(interval, rangers):
    results = []
    remaining_interval = interval
    for ranger in sorted(rangers, key=lambda r: r.start):
        if ranger.stop < remaining_interval[0] or ranger.start >= remaining_interval[1]:
            continue

        pivot_start = min(ranger.start, remaining_interval[1])
        pivot_stop = min(remaining_interval[1], ranger.stop)

        if ranger.start > remaining_interval[0]:
            results.append((remaining_interval[0], pivot_start))
            remaining_interval = (pivot_start, remaining_interval[1])
        if ranger.start <= remaining_interval[0]:
            results.append((remaining_interval[0] + ranger.delta, pivot_stop + ranger.delta))
            remaining_interval = (pivot_stop, remaining_interval[1])
        if remaining_interval[0] == remaining_interval[1]:
            remaining_interval = None
            break
    if remaining_interval:
        results.append((remaining_interval))
    return results


def part2(filepath):
    with open(filepath, 'r') as infile:
        text = infile.read()
    board = parse_board(text)

    def garden(init_intervals):
        keyname = 'seed'
        nextkey = [k for k in board if k.startswith(keyname + '_to')][0]
        intervals = init_intervals
        while nextkey:
            next_intervals = []
            for interval in intervals:
                next_intervals.extend(proc_ranges(interval, board[nextkey]))
            keyname = nextkey.split('_')[-1]
            nextkeys = [k for k in board if k.startswith(keyname + '_to')]
            nextkey = nextkeys[0] if nextkeys else None
            intervals = next_intervals
        amin = min([i[0] for i in intervals])
        bmin = min([i[1] - 1 for i in intervals])
        return min(amin, bmin)

    intervals = []
    for i in tqdm(range(int(len(board['seed']) / 2))):
        seedstart = board['seed'][i * 2]
        seedstop = seedstart + board['seed'][i * 2 + 1]
        intervals.append((seedstart, seedstop))

    print(garden(intervals))


# do_puzzle('05_01.txt')

# part2('05_test.txt')
part2('05_01.txt')
