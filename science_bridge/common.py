#!/bin/false
# -*- encoding=utf-8 -*-

import fractions

SUITS = '♣♦♥♠'
RANKS = '23456789⑩JQKA'
FACTORIALS = [1]

for i in range(1, 52 + 1):
    FACTORIALS.append(FACTORIALS[-1] * i)


def binomial(n, k):
    # There is a more efficient way, see Wikipedia.
    return FACTORIALS[n] // (FACTORIALS[k] * FACTORIALS[n - k])


# Probability of exactly three spades:
# subset_probability(52, 13, 13, 3) -> Fraction(1336935171, 4669217350)
def subset_probability(n, t, g, d):
    assert all(isinstance(x, int) for x in [n, t, g, d])
    num = binomial(g, d) * binomial(n - g, t - d)
    denom = binomial(n, t)
    assert 0 < num < denom
    return fractions.Fraction(num, denom)


def hand_2suit_probability(c, d):
    # Follows from subset_probability(…)
    assert 0 <= c <= 13
    assert 0 <= d <= 13
    assert 0 <= c + d <= 13
    num = binomial(13, c) * binomial(13, d) * binomial(52 - 13 - 13, 13 - c - d)
    denom = binomial(52, 13)
    assert 0 < num < denom
    return fractions.Fraction(num, denom)


def hand_4suit_probability(c, d, h, s):
    # Follows from subset_probability(…)
    assert all(0 <= x <= 13 for x in (c, d, h, s))
    assert c + d + h + s == 13
    num = binomial(13, c) * binomial(13, d) * binomial(13, h) * binomial(13, s)
    denom = binomial(52, 13)
    assert 0 < num < denom
    return fractions.Fraction(num, denom)


def card_suit(card_idx):
    return card_idx // 13


def card_rank(card_idx):
    return card_idx % 13


def card_to_string(card_idx):
    assert 0 <= card_idx < 52
    return SUITS[card_suit(card_idx)] + RANKS[card_rank(card_idx)]


def deal_to_string(deal):
    assert len(deal) == 52
    return ' '.join(card_to_string(card) for card in deal)
