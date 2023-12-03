import os
import re

replacements = [('one', 1),
                ('two', 2),
                ('three', 3),
                ('four', 4),
                ('five', 5),
                ('six', 6),
                ('seven', 7),
                ('eight', 8),
                ('nine', 9)]

with open('01_01.txt', 'r') as infile:
    text = infile.read()


def post_process_input(text):
    insertables = []
    for name, num in replacements:
        for match in re.finditer(name, text):
            insertables.append((match.start(), num))
    i = 0
    for pos, num in sorted(insertables, key=lambda x: x[0]):
        text = text[:pos + i] + str(num) + text[pos + i:]
        i += 1
    return text.split(os.linesep)


def get_calibrations(line):
    digits = [c for c in line if c.isnumeric()]
    return int(digits[0] + digits[-1])


lines = post_process_input(text)
print(lines)
print([get_calibrations(line) for line in lines])
print(sum([get_calibrations(line) for line in lines]))
