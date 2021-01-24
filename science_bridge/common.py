#!/bin/false
# -*- fileencoding=utf-8 -*-

SUITS = '♣♦♥♠'
RANKS = '23456789⑩JQKA'


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
