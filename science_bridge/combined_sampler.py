#!/usr/bin/env python3

import common
import math
import os
import secrets
import sys
import table
import time

FORMAT = 'str'  # 'None' or 'int' or 'str'

DEFAULT_NUM_SAMPLES = 10
REPORT_FRACTION = 10000


def print_samples(table_int, n, min_max_reqs):
    last_print = time.time()
    tries_total = 0
    last_reported_tries = 0
    i = 0
    last_reported_i = 0
    while i < n:
        if tries_total - last_reported_tries >= REPORT_FRACTION:
            this_print = time.time()
            print('iter {}, about {}/s, about {} tries/s'.format(
                    i, (i - last_reported_i) / (this_print - last_print), (tries_total - last_reported_tries) / (this_print - last_print)),
                file=sys.stderr)
            last_print = this_print
            last_reported_i = i
            last_reported_tries = tries_total
        sample_4suits = table.sample_table_int(table_int)
        sample_deal, tries = common.try_sample_deal_4suits_hpc(sample_4suits, min_max_reqs)
        tries_total += tries

        if sample_deal is None:
            continue

        i += 1

        if FORMAT == 'int':
            print(sample_deal)
        elif FORMAT == 'str':
            print(common.deal_to_string(sample_deal))
        elif FORMAT == 'None':
            pass
        else:
            raise AssertionError(FORMAT)


def run_with(num_samples, *min_max_reqs):
    assert len(min_max_reqs) == 10
    tightened_reqs = common.tighten_mmr(min_max_reqs[:8])
    if tightened_reqs != min_max_reqs[:8]:
        print('Suit requirements tightened from {} to {}'.format(min_max_reqs[:8], tightened_reqs), file=sys.stderr)
        min_max_reqs = tightened_reqs + min_max_reqs[-2:]
    entries = table.compute_table_4suits()
    entries = table.filter_table(entries, 0, min_max_reqs[0], min_max_reqs[1])
    entries = table.filter_table(entries, 1, min_max_reqs[2], min_max_reqs[3])
    entries = table.filter_table(entries, 2, min_max_reqs[4], min_max_reqs[5])
    entries = table.filter_table(entries, 3, min_max_reqs[6], min_max_reqs[7])
    # Don't even need to rescale to 1 first!
    table_int = table.rescale_table_int(entries)
    print_samples(table_int, num_samples, min_max_reqs)


if __name__ == '__main__':
    if len(sys.argv) == 1 + 10:
        run_with(DEFAULT_NUM_SAMPLES, *(int(x) for x in sys.argv[1:11]))
    elif len(sys.argv) == 1 + 10 + 1:
        run_with(int(sys.argv[-1]), *(int(x) for x in sys.argv[1:11]))
    else:
        print('USAGE: {} <MIN_MAX_REQS> [<NUM_SAMPLES>]'.format(sys.argv[0]), file=sys.stderr)
        print('MIN_MAX_REQS is 10 integers, 2 for each suit, and 2 for HPC,', file=sys.stderr)
        print('describing the minimum and maximum interesting amount.', file=sys.stderr)
        print('(Use "0" "99" for "no restriction", and "3" "3" for "exactly 3", etc.)', file=sys.stderr)
        print('NUM_SAMPLES is the number of samples to print. Defaults to {}'.format(DEFAULT_NUM_SAMPLES), file=sys.stderr)
        exit(1)
