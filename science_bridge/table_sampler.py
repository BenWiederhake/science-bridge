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


def print_samples(table_int, n):
    last_print = time.time()
    for i in range(n):
        sample_4suits = table.sample_table_int(table_int)
        sample_deal = common.sample_deal_4suits(sample_4suits)
        if FORMAT == 'int':
            print(sample_deal)
        elif FORMAT == 'str':
            print(common.deal_to_string(sample_deal))
        elif FORMAT == 'None':
            pass
        else:
            raise AssertionError(FORMAT)
        if i > 0 and i % 10000 == 0:
            this_print = time.time()
            print('iter {}, about {}/s'.format(i, 10000 / (this_print - last_print)), file=sys.stderr)
            last_print = this_print


def run_with(num_samples, *min_max_reqs):
    assert len(min_max_reqs) == 8
    tightened_reqs = common.tighten_mmr(min_max_reqs)
    if tightened_reqs != min_max_reqs:
        print('Suit requirements tightened from {} to {}'.format(min_max_reqs, tightened_reqs), file=sys.stderr)
        min_max_reqs = tightened_reqs
    entries = table.compute_table_4suits()
    entries = table.filter_table(entries, 0, min_max_reqs[0], min_max_reqs[1])
    entries = table.filter_table(entries, 1, min_max_reqs[2], min_max_reqs[3])
    entries = table.filter_table(entries, 2, min_max_reqs[4], min_max_reqs[5])
    entries = table.filter_table(entries, 3, min_max_reqs[6], min_max_reqs[7])
    # Don't even need to rescale to 1 first!
    table_int = table.rescale_table_int(entries)
    print_samples(table_int, num_samples)


if __name__ == '__main__':
    if len(sys.argv) == 1 + 8:
        run_with(DEFAULT_NUM_SAMPLES, *(int(x) for x in sys.argv[1:9]))
    elif len(sys.argv) == 1 + 8 + 1:
        run_with(int(sys.argv[9]), *(int(x) for x in sys.argv[1:9]))
    else:
        print('USAGE: {} <MIN_MAX_REQS> [<NUM_SAMPLES>]'.format(sys.argv[0]), file=sys.stderr)
        print('MIN_MAX_REQS is 8 integers, 2 for each suit, describing the minimum and maximum interesting amount.', file=sys.stderr)
        print('(Use "0" "13" for "no restriction", and "3" "3" for "exactly 3", etc.)', file=sys.stderr)
        print('NUM_SAMPLES is the number of samples to print. Defaults to {}'.format(DEFAULT_NUM_SAMPLES), file=sys.stderr)
        exit(1)
