---
layout: post
title: "Birthday Paradox and Hash Functions"
date: 2017-03-04 22:13:16 -0800
comments: true
categories:
---

The <a href="https://en.wikipedia.org/wiki/Birthday_problem" target="_blank">Birthday Problem</a> is concerned with computing the probability that, in a set of $n$ randomly chosen people, at least one pair of people will have the same birthday (let's call it a 'collision').

Intuitively, what would be your guess for the probability of collision to become > 0.5? Given that there are 365 possible days, I would imagine $n$ to be quiet large for this to happen. Let's compute it by hand.

What is the probability that there isn't a collision?

* The total number of combinations of birthdays possible for the set of $n$ people is $365^n$.
* However, for the birthdays to not overlap, each one should pick $n$ different birthdays out of the 365 possible ones. This is equal to $\_{365}P\_{n}$ (pick any $n$ out of the 365 days, and allow permutations).

* $P(\text{no collision}) = \frac{\_{365}P\_{n}}{365^n}$.

* $P(\text{collision}) = 1 - \frac{\_{365}P\_{n}}{365^n}$.

Plotting the graph for collision to happen, let's see where this becomes true.

<!-- center -->
![n vs p(collision)]({{ site.baseurl }}/assets/img/2017/03/04/birthday_paradox.png)

So it seems that the collision happens with a probability >= 0.5 after $n$ is greater than 23. The paradox in the Birthday Paradox is that we expect $n$ to be quite large, where as it seems you need only $\approx \sqrt{365}$ people.

In general, it has been proven that the if there are $n$ balls, and $b$ bins, then the probability of any bin having > 1 ball is >= 0.5, when $n \approx \sqrt{b}$.

<a href="https://en.wikipedia.org/wiki/Birthday_attack" target="_blank">Considering hash functions to be placing balls in bins</a>, if the number of distinct elements that could be fed to the hash function are $n$, to ensure that the probability of collision remains < 0.5, the length of the hash in number of bits required for the hash function, $l$, should be such that $2^l > n^2$.

This means, if you expect $2^{32}$ distinct elements, make sure to use at least a 64 bit hash, if you want the probability of collision to be < 0.5
