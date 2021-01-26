# science-bridge

> Combining Science and the card game Bridge since right now.

This library supports various probabilistic analyses of a Bridge deal, for example:
- Q: "How probable is it that North gets exactly 3 Spades?"
  A: Exactly 1336935171 / 4669217350, or roughly 28.63296%
- Q: "How probable is it that North gets 2-5 Spades and 3-6 Hearts?"
  A: FIXME
- Q: "If North has 3-4 Spades and 2-6 Hearts, how probable is it that they receive 1-7 Clubs?"
  A: FIXME
- Q: "Show me a uniformly randomly sampled deal where North gets 1-3 Clubs, 3-5 Diamonds, 3-7 Hearts, 3-6 Spades, and a total of 12-16 High Point Cards!"
  A: FIXME

![A caption of Jesse Pinkman from Breaking Bad saying "Yeah! Science Bridge!"](https://i.imgflip.com/4uzlba.jpg)

## Table of Contents

- [Background](#background)
- [Install](#install)
- [Usage](#usage)
- [Performance](#performance)
- [TODOs](#todos)
- [NOTDOs](#notdos)
- [Contribute](#contribute)
- [License](#license)

## Background

There are 52 cards in a deck, each card has a suit (♣♦♥♠) and rank (23456789⑩JQKA), and each combination occurs exactly once.

A deal is an assignment of the 52 cards in a deck to the 4 players such that
each player receives 13 cards; the ordering of cards of a player's hand does
not matter. Ordinarily, the deck is shuffled (each permutation of cards in the
deck is assumed to be equally likely) before dealing.

Sampling from a discrete distribution with a known CDF (cumulative distribution function) is easy. Also, if we can partition the probability space into disjoint events, we can just "set" the probability for the undesired events to 0, rescale the remaining probabilities, and go to town.
- Note that this trick does not work as-is for conditional probabilities. Therefore, it is necessary to compute absolute probabilities.
- Note that IEEE754 causes some rounding to occur. I don't know how that error would propagate, and since this project involves adding numbers of wildly different magnitude (the weak point of IEEE754), it is necessary to deal with rationals (think "bignums") instead.

## Install

FIXME

## Usage

FIXME

Just Python for now

## Performance

FIXME

If necessary, I may consider rewriting some parts in Rust.

## TODOs

* Probability calculator
* Table generator
* Actual sampler
* Monte-Carlo stuff for the rank conditions
* Update Readme with actual data

## NOTDOs

These aren't meant as strict rules, but I most definitely won't implement these things:
* Actual bridge rules.
* Game engine.
* GUI.
* Web interface.

## Contribute

Feel free to dive in! [Open an issue](https://github.com/BenWiederhake/science-bridge/issues/new) or submit PRs.

## License

[Attribution-NonCommercial-NoDerivatives 4.0 International (CC BY-NC-ND 4.0) ](https://creativecommons.org/licenses/by-nc-nd/4.0/).

In particular, note that you may not use the material for commercial purposes.
Feel free to [contact](https://github.com/BenWiederhake/science-bridge/issues/new) me with offers.

A copy of the full license text can be found in `LICENSE`.
