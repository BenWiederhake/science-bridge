# science-bridge

> Combining Science and the card game Bridge since right now.

This library supports various probabilistic analyses of a Bridge deal, for example:
- Q: "How probable is it that North gets exactly 3 Spades?"
  A: Exactly 1336935171 / 4669217350, or roughly 28.63296%
- Q: "How probable is it that North gets 2-5 Spades and 3-6 Hearts?"
  A: Exactly 437833539 / 738387860, or roughly 59.29587 %
- Q: "If North has 3-4 Spades and 2-6 Hearts, how probable is it that they receive at least 5 Clubs?"
  A: Exactly 47039 / 378210, or roughly 12.43727 %
- Q: "Show me a uniformly randomly sampled deal where North gets 1-3 Clubs, 3-5 Diamonds, 3-7 Hearts, 3-6 Spades!"
  A: ♣2 ♣6 ♦3 ♦7 ♦J ♥4 ♥5 ♥9 ♥Q ♠2 ♠3 ♠6 ♠Q   ♣5 ♣9 ♣Q ♣A ♦5 ♦9 ♦⑩ ♦Q ♦K ♥7 ♠7 ♠J ♠A   ♣3 ♣7 ♣⑩ ♣K ♦4 ♥2 ♥3 ♥8 ♥K ♥A ♠4 ♠5 ♠⑩   ♣4 ♣8 ♣J ♦2 ♦6 ♦8 ♦A ♥6 ♥⑩ ♥J ♠8 ♠9 ♠K
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

Here's a uniformly sampled deal:

- North: ♣6 ♣J ♣Q ♣K ♣A ♦Q ♥2 ♥8 ♥9 ♠2 ♠⑩ ♠Q ♠A
- East: ♣4 ♣5 ♦2 ♦3 ♦J ♦A ♥5 ♥7 ♥Q ♥K ♠3 ♠9 ♠J
- South: ♣3 ♣7 ♣⑩ ♦4 ♦5 ♦8 ♦⑩ ♥6 ♥J ♥A ♠4 ♠6 ♠7
- West: ♣2 ♣8 ♣9 ♦6 ♦7 ♦9 ♦K ♥3 ♥4 ♥⑩ ♠5 ♠8 ♠K

A deal is an assignment of the 52 cards in a deck to the 4 players such that
each player receives 13 cards; the ordering of cards of a player's hand does
not matter. Ordinarily, the deck is shuffled (each permutation of cards in the
deck is assumed to be equally likely) before dealing.

Sampling from a discrete distribution with a known CDF (cumulative distribution function) is easy. Also, if we can partition the probability space into disjoint events, we can just "set" the probability for the undesired events to 0, rescale the remaining probabilities, and go to town.
- Note that this trick does not work as-is for conditional probabilities. Therefore, it is necessary to compute absolute probabilities.
- Note that IEEE754 causes some rounding to occur. I don't know how that error would propagate, and since this project involves adding numbers of wildly different magnitude (the weak point of IEEE754), it is necessary to deal with rationals (think "bignums") instead.

## Install

You need python 3.7 or newer. No custom packages necessary.

## Usage

FIXME

Just Python for now

### Examples in the intro

##### Q: "How probable is it that North gets exactly 3 Spades?"

```
>>> import table
>>> table.compute_table_1suit()[(3,)]
Fraction(1336935171, 4669217350)
>>> float(_)
0.2863296074662277
>>>
```

##### Q: "How probable is it that North gets 2-5 Spades and 3-6 Hearts?"

```
>>> interesting_entries = table.compute_table_2suits()
>>> interesting_entries = table.filter_table(interesting_entries, 0, 2, 5)
>>> interesting_entries = table.filter_table(interesting_entries, 1, 3, 6)
>>> sum(interesting_entries.values())
Fraction(437833539, 738387860)
>>> float(_)
0.5929587452859801
>>>
```

##### Q: "If North has 3-4 Spades and 2-6 Hearts, how probable is it that they receive at least 5 Clubs?"

```
>>> interesting_entries = table.compute_table_4suits()
>>> interesting_entries = table.filter_table(interesting_entries, 0, 3, 4)
>>> interesting_entries = table.filter_table(interesting_entries, 1, 2, 6)
>>> clubby_entries = table.filter_table(interesting_entries, 2, 5, 13)
>>> sum(clubby_entries.values()) / sum(interesting_entries.values())
Fraction(47039, 378210)
>>> float(_)
0.12437270299569023
>>>
```

##### Q: "Show me a uniformly randomly sampled deal where North gets 1-3 Clubs, 3-5 Diamonds, 3-7 Hearts, 3-6 Spades!"

```
$ ./table_sampler.py 1 3 3 5 3 7 3 6
♣2 ♣6 ♦3 ♦7 ♦J ♥4 ♥5 ♥9 ♥Q ♠2 ♠3 ♠6 ♠Q   ♣5 ♣9 ♣Q ♣A ♦5 ♦9 ♦⑩ ♦Q ♦K ♥7 ♠7 ♠J ♠A   ♣3 ♣7 ♣⑩ ♣K ♦4 ♥2 ♥3 ♥8 ♥K ♥A ♠4 ♠5 ♠⑩   ♣4 ♣8 ♣J ♦2 ♦6 ♦8 ♦A ♥6 ♥⑩ ♥J ♠8 ♠9 ♠K
♣7 ♣⑩ ♦4 ♦Q ♦A ♥2 ♥8 ♥⑩ ♥K ♠5 ♠9 ♠⑩ ♠J   ♣5 ♣8 ♣9 ♣A ♦2 ♦6 ♦8 ♦J ♥7 ♥J ♠6 ♠8 ♠Q   ♣Q ♣K ♦3 ♦9 ♦⑩ ♦K ♥4 ♥5 ♥9 ♥Q ♠3 ♠4 ♠K   ♣2 ♣3 ♣4 ♣6 ♣J ♦5 ♦7 ♥3 ♥6 ♥A ♠2 ♠7 ♠A
♣2 ♣8 ♣K ♦3 ♦4 ♦J ♥7 ♥9 ♥Q ♠6 ♠7 ♠8 ♠K   ♣6 ♣Q ♦2 ♦5 ♦7 ♦Q ♦K ♦A ♥⑩ ♥J ♥A ♠5 ♠Q   ♣3 ♣7 ♣9 ♣J ♦6 ♥2 ♥3 ♥4 ♥5 ♥6 ♥8 ♠2 ♠A   ♣4 ♣5 ♣⑩ ♣A ♦8 ♦9 ♦⑩ ♥K ♠3 ♠4 ♠9 ♠⑩ ♠J
♣9 ♣⑩ ♣A ♦2 ♦⑩ ♦J ♥2 ♥5 ♥K ♠3 ♠8 ♠K ♠A   ♣3 ♦3 ♦6 ♦9 ♦K ♥6 ♥J ♥Q ♥A ♠2 ♠5 ♠⑩ ♠J   ♣5 ♣7 ♣8 ♣K ♦5 ♦A ♥3 ♥4 ♥7 ♥9 ♥⑩ ♠6 ♠Q   ♣2 ♣4 ♣6 ♣J ♣Q ♦4 ♦7 ♦8 ♦Q ♥8 ♠4 ♠7 ♠9
♣3 ♣5 ♣A ♦2 ♦6 ♦K ♥3 ♥5 ♥6 ♥9 ♠3 ♠6 ♠J   ♣4 ♣K ♦3 ♦7 ♦8 ♦9 ♦J ♦A ♥2 ♥4 ♥8 ♠2 ♠K   ♣6 ♣7 ♣8 ♣⑩ ♣Q ♦5 ♦⑩ ♥Q ♥K ♥A ♠4 ♠5 ♠A   ♣2 ♣9 ♣J ♦4 ♦Q ♥7 ♥⑩ ♥J ♠7 ♠8 ♠9 ♠⑩ ♠Q
♣2 ♣Q ♦3 ♦9 ♦Q ♥3 ♥6 ♥A ♠2 ♠3 ♠5 ♠8 ♠A   ♣3 ♣6 ♣⑩ ♣J ♦4 ♦J ♦K ♥2 ♥7 ♥J ♥K ♠⑩ ♠Q   ♣4 ♣7 ♣K ♦5 ♦7 ♦8 ♦⑩ ♥4 ♥5 ♥8 ♥9 ♠9 ♠J   ♣5 ♣8 ♣9 ♣A ♦2 ♦6 ♦A ♥⑩ ♥Q ♠4 ♠6 ♠7 ♠K
♣7 ♣Q ♦5 ♦⑩ ♦K ♥3 ♥4 ♥9 ♠2 ♠8 ♠⑩ ♠J ♠K   ♣2 ♣6 ♣J ♦2 ♦3 ♦7 ♥J ♥Q ♥K ♥A ♠3 ♠9 ♠A   ♣3 ♣4 ♣5 ♣K ♦6 ♦9 ♦J ♦A ♥2 ♥8 ♠4 ♠5 ♠7   ♣8 ♣9 ♣⑩ ♣A ♦4 ♦8 ♦Q ♥5 ♥6 ♥7 ♥⑩ ♠6 ♠Q
♣3 ♦4 ♦6 ♦8 ♦J ♦Q ♥7 ♥⑩ ♥A ♠5 ♠8 ♠9 ♠J   ♣2 ♣4 ♣7 ♣8 ♣9 ♣J ♦5 ♦A ♥8 ♥Q ♠2 ♠3 ♠A   ♣6 ♣Q ♣A ♦2 ♦3 ♦7 ♦K ♥2 ♥4 ♥5 ♥9 ♠⑩ ♠Q   ♣5 ♣⑩ ♣K ♦9 ♦⑩ ♥3 ♥6 ♥J ♥K ♠4 ♠6 ♠7 ♠K
♣2 ♣⑩ ♣Q ♦2 ♦3 ♦6 ♦8 ♥6 ♥8 ♥Q ♠3 ♠4 ♠6   ♣5 ♣6 ♣9 ♣A ♦4 ♦7 ♦⑩ ♦J ♦K ♥9 ♥J ♥K ♠A   ♣3 ♣4 ♣7 ♣8 ♣K ♦Q ♦A ♥3 ♥7 ♠8 ♠9 ♠⑩ ♠K   ♣J ♦5 ♦9 ♥2 ♥4 ♥5 ♥⑩ ♥A ♠2 ♠5 ♠7 ♠J ♠Q
♣3 ♣7 ♣8 ♦2 ♦3 ♦5 ♥5 ♥6 ♥K ♠4 ♠⑩ ♠J ♠A   ♣5 ♣K ♦4 ♦6 ♦8 ♦9 ♦Q ♥4 ♥7 ♥8 ♥A ♠5 ♠6   ♣9 ♣⑩ ♣A ♦⑩ ♦K ♦A ♥3 ♥9 ♥Q ♠3 ♠7 ♠8 ♠K   ♣2 ♣4 ♣6 ♣J ♣Q ♦7 ♦J ♥2 ♥⑩ ♥J ♠2 ♠9 ♠Q
```

FIXME

##### Q: "Show me a uniformly randomly sampled deal where North gets 1-3 Clubs, 3-5 Diamonds, 3-7 Hearts, 3-6 Spades, and a total of 12-16 High Point Cards!"

FIXME

## Performance

- The naive sampler (which can only sample from *all* deals) written in Python runs at around 10 K/s.
- The table-based sampler (which can only sample from *suit-constrained* deals) written in Python should run at about the same speed, albeit a bit slower. I expect 9 K/s.
- The general sampler (which can sample from arbitrary deals) will have to employ Monte Carlo sampling, and has therefore far lower, and unpredictable speed.

If necessary, I may consider rewriting some parts in Rust.

FIXME

## TODOs

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
