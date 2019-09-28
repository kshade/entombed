#!/usr/bin/env python

# Python 3
# see LICENSE file for licensing information

import random


def get_random_bit():
    return random.randint(0, 1)


def left_random_bit():
    return get_random_bit()


def right_random_bit():
    return get_random_bit()


def generated(x):
    pass


solid = '██'
empty = '..'


def pr_row(seed):
    pf12 = ''
    for i in range(8):
        if seed & 1:
            pf12 = solid + pf12
        else:
            pf12 = empty + pf12
        seed >>= 1
    pf012 = solid * 2 + pf12

    print(pf012 + pf012[::-1])


green = '\033[1;32;40m'
cyan = '\033[1;36;40m'
red = '\033[1;31;40m'
purple = '\033[1;35;40m'
yellow = '\033[1;33;40m'
reset = '\033[0;0m'
coloured = {'S': green + solid,
            'E': green + empty,
            'R': cyan + solid,
            'A': red + empty,
            'B': red + solid,
            'C': purple + solid,
            'D': purple + empty
            }

# Print rows marked with ANSI colours
def pr_row_marked(halfrow):
    fullrow = halfrow + halfrow[::-1]
    ansirow = yellow + solid + solid

    for tile in fullrow:
        ansirow = ansirow + coloured[tile]

    ansirow = ansirow + yellow + solid + solid + reset

    print(ansirow)


# the mystery table from Entombed
# Rearranged to match the folded and rotated one
# 'S' Solid on left side of table, empty on right
# 'E' As above but inverse
# 'R' Random either side of table
# 'A', 'B' Empty on left, random on right side of table
# 'C', 'D' Random on left, empty on right side of table

MAGIC = {
    (0b00, 0b000): 'S',  (0b11, 0b111): 'E', # Inverse bits, inverse result
    (0b00, 0b001): 'S',  (0b11, 0b110): 'E',
    (0b00, 0b010): 'S',  (0b11, 0b101): 'E',
    (0b00, 0b011): 'R',  (0b11, 0b100): 'R', # Random on both sides...
    (0b00, 0b100): 'A',  (0b11, 0b011): 'B', # except here...
    (0b00, 0b101): 'E',  (0b11, 0b010): 'S',
    (0b00, 0b110): 'C',  (0b11, 0b001): 'D', # and here
    (0b00, 0b111): 'R',  (0b11, 0b000): 'R',

    (0b01, 0b000): 'S',  (0b10, 0b111): 'E',
    (0b01, 0b001): 'S',  (0b10, 0b110): 'E',
    (0b01, 0b010): 'S',  (0b10, 0b101): 'E',
    (0b01, 0b011): 'S',  (0b10, 0b100): 'E',
    (0b01, 0b100): 'R',  (0b10, 0b011): 'R',
    (0b01, 0b101): 'E',  (0b10, 0b010): 'S',
    (0b01, 0b110): 'E',  (0b10, 0b001): 'S',
    (0b01, 0b111): 'E',  (0b10, 0b000): 'S',
}

# Translates the modified table back to bits.
# Random is always 1 (determined by fair coin toss)
translation = {'S': 1, 'E': 0, 'R': 1, 'A': 0, 'B': 1, 'C': 1, 'D': 0}


def row_gen(last_rows):
    # prepend and append random bits to last row
    last_row_padded = left_random_bit()
    last_row_padded <<= 8
    last_row_padded |= last_rows[-1]
    last_row_padded <<= 1
    last_row_padded |= right_random_bit()

    # last two bits generated in current row, initial value = 10
    last_two = 0b10

    new_row = 0
    new_row_marked = ''

    # iterate from 7...0, inclusive
    for i in range(7, -1, -1):
        three_above = (last_row_padded >> i) & 0b111

        new_bit_marked = MAGIC[last_two, three_above]
        new_bit = translation[new_bit_marked]

        new_row_marked = new_row_marked + new_bit_marked
        new_row = (new_row << 1) | new_bit

        last_two = ((last_two << 1) | new_bit) & 0b11

    # hook for verification
    generated(new_row)

    # now do postprocessing
    last_rows.append(new_row)
    last_rows = last_rows[-11:]

    # condition 1
    history = [b & 0xf0 for b in last_rows]
    if 0 not in history:
        if sum([b & 0x80 for b in history]) == 0:
            # print 'pp 1'
            last_rows[-1] = 0

    # condition 2
    history = [b & 0xf for b in last_rows[-7:]]
    if 0 not in history:
        comparator = 0
        if len(last_rows) >= 9:
            comparator = last_rows[-9]
        if sum([b & 1 for b in history]) == (comparator & 1) * 7:
            # print 'pp 2'
            last_rows[-1] &= 0xf0

    #pr_row(last_rows[-1])
    pr_row_marked(new_row_marked)
    return last_rows


def maze_gen():
    last_rows = [0]
    while True:
        last_rows = row_gen(last_rows)


if __name__ == '__main__':
    # random.seed(12345)
    maze_gen()
