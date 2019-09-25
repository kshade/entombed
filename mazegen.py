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


def mid_random_bit():
    return get_random_bit()


def generated(x):
    pass


solid = 'XX'
empty = '__'


def pr_row(seed):
    pf12 = ''
    for i in range(8):
        if seed & 1:
            pf12 = solid + pf12
        else:
            pf12 = empty + pf12
        seed >>= 1
    pf012 = solid * 2 + pf12

    print(pf012, pf012[::-1])


# the mystery table from Entombed

MAGIC = {
    (0b00, 0b000): 1,
    (0b00, 0b001): 1,
    (0b00, 0b010): 1,
    (0b00, 0b011): None,  # None == random bit
    (0b00, 0b100): 0,
    (0b00, 0b101): 0,
    (0b00, 0b110): None,
    (0b00, 0b111): None,

    (0b01, 0b000): 1,
    (0b01, 0b001): 1,
    (0b01, 0b010): 1,
    (0b01, 0b011): 1,
    (0b01, 0b100): None,
    (0b01, 0b101): 0,
    (0b01, 0b110): 0,
    (0b01, 0b111): 0,

    (0b10, 0b000): 1,
    (0b10, 0b001): 1,
    (0b10, 0b010): 1,
    (0b10, 0b011): None,
    (0b10, 0b100): 0,
    (0b10, 0b101): 0,
    (0b10, 0b110): 0,
    (0b10, 0b111): 0,

    (0b11, 0b000): None,
    (0b11, 0b001): 0,
    (0b11, 0b010): 1,
    (0b11, 0b011): None,
    (0b11, 0b100): None,
    (0b11, 0b101): 0,
    (0b11, 0b110): 0,
    (0b11, 0b111): 0,
}


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

    # iterate from 7...0, inclusive
    for i in range(7, -1, -1):
        three_above = (last_row_padded >> i) & 0b111

        new_bit = MAGIC[last_two, three_above]
        if new_bit is None:
            new_bit = mid_random_bit()
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

    pr_row(last_rows[-1])
    return last_rows


def maze_gen():
    last_rows = [0]
    while True:
        last_rows = row_gen(last_rows)


if __name__ == '__main__':
    # random.seed(12345)
    maze_gen()
