#!/usr/bin/env python3

import atomicwrites
import collections
import common
import json
import random
import secrets  # If this fails, update to python 3.7 or newer
import time


INCREMENT = 10000


def generate_deals():
    l = list(range(52))
    while True:
        # Why is this being deprecated, and how to generate secure shuffles?
        random.shuffle(l, secrets.SystemRandom().random)
        yield l
        assert len(l) == 52, 'Ey!'


def do_time_self():
    gen = generate_deals()
    new_time = time.time()
    suit_counts = collections.Counter()
    filename = time.strftime('empiric_counts_%s.json')
    total = 0
    while True:
        for _ in range(INCREMENT):
            hand_suit_counts = collections.Counter(i // 13 for i in next(gen)[:13])
            assert hand_suit_counts[0] + hand_suit_counts[1] + hand_suit_counts[2] + hand_suit_counts[3] == 13
            suit_counts[hand_suit_counts[0] * 1000000 + hand_suit_counts[1] * 10000 + hand_suit_counts[2] * 100 + hand_suit_counts[3]] += 1
        total += INCREMENT
        last_time = new_time
        new_time = time.time()
        print('{} ms / iter – {}: {}'.format(
            1000 * (new_time - last_time) / INCREMENT,
            total,
            suit_counts.most_common()[:20]))
        with atomicwrites.atomic_write(filename, overwrite=True) as fp:
            json.dump([total, suit_counts], fp, separators=',:')


if __name__ == '__main__':
    print(common.deal_to_string(next(generate_deals())))
    do_time_self()
