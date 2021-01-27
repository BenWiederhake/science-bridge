#!/bin/false
# -*- encoding=utf-8 -*-

import fractions
import random
import secrets

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
    display_deal = []
    for hand in range(4):
        hand_cards = deal[13 * hand:13 * (hand + 1)]
        hand_cards.sort()
        display_deal.append(hand_cards)
    return '   '.join(' '.join(card_to_string(card) for card in hand) for hand in display_deal)


def shuffle_inplace(l):
    # Why is this being deprecated, and how to generate secure shuffles?
    random.shuffle(l, secrets.SystemRandom().random)


def sample_deal_4suits(count_4suits):
    assert len(count_4suits) == 4
    assert sum(count_4suits) == 13

    cards_by_suit = []
    for i in range(4):
        in_suit = list(range(13 * i, 13 * (i + 1)))
        shuffle_inplace(in_suit)
        cards_by_suit.append(in_suit)
    # `cards_by_suit` is a list of list of cards!

    deal = []
    # First, deal North's cards:
    for suit_idx, suit_count in zip(range(4), count_4suits):
        # TODO: This looks inefficient
        for _ in range(suit_count):
            deal.append(cards_by_suit[suit_idx].pop())
    assert len(deal) == 13

    # Then, deal the rest randomly:
    remaining_cards = []
    for suit_cards in cards_by_suit:
        remaining_cards.extend(suit_cards)
    del suit_cards
    shuffle_inplace(remaining_cards)
    deal.extend(remaining_cards)

    return deal


def count_hpc(cards):
    return sum(max(0, card_rank(i) - 8) for i in cards)


def last_x_slice(l, x):
    if x == 0:
        return []
    assert 0 < x < len(l)
    return l[-x:]


def try_sample_deal_4suits_hpc(count_4suits, min_max_reqs):
    assert len(count_4suits) == 4
    assert sum(count_4suits) == 13
    assert len(min_max_reqs) == 10

    tries = 0
    while True:
        tries += 1
        # `cards_by_suit` is a list of list of cards!
        cards_by_suit = []
        min_hpc = 0
        max_hpc = 0
        for i in range(4):
            in_suit = list(range(13 * i, 13 * (i + 1)))
            shuffle_inplace(in_suit)
            min_tail = last_x_slice(in_suit, min_max_reqs[i * 2 + 0])
            max_tail = last_x_slice(in_suit, min_max_reqs[i * 2 + 1])
            min_hpc += count_hpc(min_tail)
            max_hpc += count_hpc(max_tail)
            cards_by_suit.append(in_suit)
        # If we already know that this shuffling of ranks is impossible in all
        # cases, independent of the specific count_4suits, then we can retry
        # immediately without screwing up the probabilities.
        if min_hpc > min_max_reqs[-1]:
            # We will definitely overshoot. Retry.
            pass
        elif max_hpc < min_max_reqs[-2]:
            # We will definitely undershoot. Retry.
            pass
        else:
            # This *may* be a good deal.
            break

    assert len(cards_by_suit) == 4, len(cards_by_suit)
    deal = []
    # First, deal North's cards:
    for suit_idx, suit_count in zip(range(4), count_4suits):
        # TODO: This looks inefficient
        for _ in range(suit_count):
            deal.append(cards_by_suit[suit_idx].pop())
    assert len(deal) == 13

    # Then, deal the rest randomly:
    remaining_cards = []
    for suit_cards in cards_by_suit:
        remaining_cards.extend(suit_cards)
    del suit_cards
    shuffle_inplace(remaining_cards)
    deal.extend(remaining_cards)
    assert len(deal) == 52
    assert set(deal) == set(range(52))

    # Did this mess it up?
    actual_hpc = count_hpc(deal[:13])
    assert min_hpc <= actual_hpc <= max_hpc, (tries, actual_hpc, count_4suits, deal)
    if actual_hpc < min_max_reqs[-2] or actual_hpc > min_max_reqs[-1]:
        # Yup, we missed the mark. Cannot retry here, or we would mess up the
        # probability for the current `count_4suits`.
        return None, tries

    return deal, tries


def tighten_mmr(min_max_reqs):
    min_max_reqs = list(min_max_reqs)  # Copy
    # There's a better way to compute this.
    change = True
    while change:
        change = False
        for i in range(4):
            total_min = min_max_reqs[0] + min_max_reqs[2] + min_max_reqs[4] + min_max_reqs[6]
            total_max = min_max_reqs[1] + min_max_reqs[3] + min_max_reqs[5] + min_max_reqs[7]
            alt_min = 13 - (total_max - min_max_reqs[2 * i + 1])
            if alt_min > min_max_reqs[2 * i + 0]:
                min_max_reqs[2 * i + 0] = alt_min
                change = True
            alt_max = 13 - (total_min - min_max_reqs[2 * i + 0])
            if alt_max < min_max_reqs[2 * i + 1]:
                min_max_reqs[2 * i + 1] = alt_max
                change = True

    return tuple(min_max_reqs)
