#!/usr/bin/env python3

import collections
import common
import fractions
import json
import math
import os


CHI_QUANTILE_STEPS = [0.002, 0.02, 0.05, 0.1, 0.2, 0.8, 0.9, 0.95, 0.98, 0.998]
CHI_QUANTILE_VALUES = {
    # Taken from https://www.itl.nist.gov/div898/handbook/eda/section3/eda3674.htm
    13: (2.617, 4.107, 5.009, 5.892, 7.042, 19.812, 22.362, 24.736, 27.688, 34.528),
    # Taken from https://mathcracker.com/chi-square-critical-values#results
    104: (65.054, 73.413, 77.672, 81.468, 85.998, 122.858, 128.804, 134.111, 140.459, 154.314),
    559: (461.344, 484.168, 495.38, 505.162, 516.6, 602.256, 615.112, 626.408, 639.713, 668.05),
}

# 'alpha', or p-value, is the probability with which we falsely reject the null hypothesis.
# Let's go at this sentence more slowly:
# - The null hypothesis is "the empirical data agrees with the computed probabilities".
# - We use the chi-squared test in several ways to try and reject the null hypothesis.
# - We want to make it as easy to reject the null hypothesis as possible, while keeping the probability of falsely rejecting the null hypothesis small.
# - For example, alpha = 0.01 means If the null hypothesis is true (the computed probabilities are correct), there is a 1 % chance that we reject it anyway.
# - In each test! So if we run 4+6+1 = 11 tests, we should use an accordingly small alpha.
# - Note that alpha does not say anything about the other way around; rest assured that that's what the chi-squared test is known to be good at.
# - A large alpha (close to 0.5) means we are quick to judge the data to be in disagreement. Therefore, the result "disagreement" doesn't say much. However, the result "agreement" would be very strong.
# - A small alpha (close to 0) means we need a lot of discrepancy before we admit disagreement. Therefore, the result "disagreement" is very strong. However, the result "agreement" doesn't say too much.
# - This is an index "from both sides" into CHI_QUANTILE_STEPS:
#   * Use 0 to reject with alpha = 0.002 / 2
#   * Use 1 to reject with alpha = 0.02 / 2
#   * Use 2 to reject with alpha = 0.05 / 2
QUANTILE_REQUIRE = 2


# == No configuration beyond this point ==


# The three compute_table_* functions could probably be written in a more abstract way;
# but I do it the "stupid" way to reduce likelihood of errors.

def compute_table_1suit():
    table = dict()
    akku = fractions.Fraction()
    for i in range(13 + 1):
        p = common.subset_probability(52, 13, 13, i)
        table[(i,)] = p
        akku += p
    assert akku == 1, akku
    return table


def gen_2suits_counts():
    for c in range(13 + 1):
        for d in range(13 - c + 1):
            yield (c, d)


def compute_table_2suits():
    table = dict()
    akku = fractions.Fraction()
    for suit_counts in gen_2suits_counts():
        p = common.hand_2suit_probability(*suit_counts)
        table[suit_counts] = p
        akku += p
    assert akku == 1, akku
    return table


def gen_4suits_counts():
    for c in range(13 + 1):
        for d in range(13 - c + 1):
            for h in range(13 - c - d + 1):
                s = 13 - c - d - h
                assert 0 <= s <= 13
                yield (c, d, h, s)


def compute_table_4suits():
    table = dict()
    akku = fractions.Fraction()
    for cdhs_counts in gen_4suits_counts():
        p = common.hand_4suit_probability(*cdhs_counts)
        table[cdhs_counts] = p
        akku += p
    assert akku == 1, akku
    return table


def run_sanity_checks():
    print('Running sanity checks ...')
    print('  Checking chi square critical values table ...')
    for q_values in CHI_QUANTILE_VALUES.values():
        assert len(CHI_QUANTILE_STEPS) == len(q_values)
    print('  Checking 1 suit table ...')
    assert len(compute_table_1suit()) == 13 + 1
    assert 13 in CHI_QUANTILE_VALUES
    print('  Checking 2 suits table ...')
    assert len(compute_table_2suits()) == 105
    assert (105 - 1) in CHI_QUANTILE_VALUES
    print('  Checking 4 suits table ...')
    assert len(compute_table_4suits()) == 560
    assert (560 - 1) in CHI_QUANTILE_VALUES
    print('  Done')


def collapse(table_in, mask):
    assert len(mask) == 4
    table_out = collections.defaultdict(int)
    for foursuits_count, value in table_in.items():
        assert len(foursuits_count) == 4
        key = tuple(c for c, take in zip(foursuits_count, mask) if take)
        table_out[key] += value
    return table_out


def is_consistent(actual, total, expected):
    #print('      KEY: ACTUAL, EXPECTED (EXPECTED) -> CHI SQUARED PART')
    chisq = 0
    viol_lt_5 = 0
    viol_lt_1 = 0
    for k, v_expected in expected.items():
        v_expected = v_expected * total
        if v_expected < 5:
            viol_lt_5 += 1
        if v_expected < 1:
            viol_lt_1 += 1
        v_actual = actual[k]
        chisq_part = (v_actual - v_expected) * (v_actual - v_expected) / v_expected
        chisq += chisq_part
        if len(expected) <= 14:
            print('      {}: {}, {} -> {}'.format(
                k,
                v_actual, float(v_expected),
                float(chisq_part),
            ))
    print('      chi squared: {} ({})'.format(chisq, float(chisq)))
    sorted_values = list(expected.values())
    sorted_values.sort()
    q_0_05 = sorted_values[math.floor(0.05 * len(sorted_values))]
    q_0_00 = sorted_values[0]
    if viol_lt_1 > 0:
        print('      ERROR: {} out of {} expected values were less than 1'.format(viol_lt_1, len(expected)))
        print('        To reach 95% >= 1, need n >= {} (5%-percentile is {})'.format(math.ceil(1 / q_0_05), q_0_05))
        print('        To reach 100% >= 1, need n >= {} (0%-percentile is {})'.format(math.ceil(1 / q_0_00), q_0_00))
    if viol_lt_5 / len(expected) >= 0.2:
        print('      WARNING: {} out of {} expected values were less than 5 ({}%)'.format(viol_lt_5, len(expected), viol_lt_5 * 100 / len(expected)))
        print('        To reach 95% >= 5, need n >= {} (5%-percentile is {})'.format(math.ceil(5 / q_0_05), q_0_05))
        print('        To reach 100% >= 5, need n >= {} (0%-percentile is {})'.format(math.ceil(5 / q_0_00), q_0_00))
    print('      For comparison:')
    pairs = list(zip(CHI_QUANTILE_STEPS, CHI_QUANTILE_VALUES[len(actual) - 1]))
    print('        {}'.format(' '.join('{}@{}'.format(q, v) for q, v in pairs)))
    print('      checking {} < {} < {}'.format(pairs[QUANTILE_REQUIRE][1], chisq, pairs[-1 - QUANTILE_REQUIRE][1]))
    return pairs[QUANTILE_REQUIRE][1] < chisq < pairs[-1 - QUANTILE_REQUIRE][1]


def run_consistency_checks(actual_table, total):
    print('Checking consistency with empiric data ...')

    print('  Checking 1 suit table ...')
    expected = compute_table_1suit()
    for i in range(4):
        mask = [False] * 4
        mask[i] = True
        actual = collapse(actual_table, mask)
        print('    suit #{}'.format(i))
        assert is_consistent(actual, total, expected)

    print('  Checking 2 suits table ...')
    expected = compute_table_2suits()
    for i in range(4):
        for j in range(i + 1, 4):
            assert i < j
            mask = [False] * 4
            mask[i] = True
            mask[j] = True
            actual = collapse(actual_table, mask)
            print('    mask {}'.format(mask))
            assert is_consistent(actual, total, expected)

    print('  Checking 4 suits table ...')
    expected = compute_table_4suits()
    assert is_consistent(collections.defaultdict(int, actual_table), total, expected)

    print('  Done')


def parse_key(k):
    k = int(k)
    # JSON doesn't support tuples as dictionary keys.
    # Hence, we encoded the numbers c, d, h, s by decimal concatenation.
    # For example, 01020304 means 1 club, 2 diamonds, 3 hearts, 4 spades.
    assert 13 <= k <= 13000000
    c = (k // 1e0) % 100
    d = (k // 1e2) % 100
    h = (k // 1e4) % 100
    s = (k // 1e6) % 100
    assert all(0 <= x <= 13 for x in [c, d, h, s])
    assert c + d + h + s == 13
    return (c, d, h, s)


def run(filename):
    run_sanity_checks()
    with open(filename, 'r') as fp:
        total, keyvals = json.load(fp)
    assert total == sum(keyvals.values())
    actual_table = {parse_key(k): v for k, v in keyvals.items()}
    run_consistency_checks(actual_table, total)


if __name__ == '__main__':
    import sys
    if len(sys.argv) == 1:
        run_sanity_checks()
        print('Run with an empiric-counts json file as argument to check consistency with empiric data.', file=sys.stderr)
    elif len(sys.argv) != 2 or not os.path.exists(sys.argv[1]):
        print('Usage: {} <EMPIRIC_COUNTS_JSON_FILE>'.format(sys.argv[0]), file=sys.stderr)
        exit(1)
    else:
        run(sys.argv[1])
