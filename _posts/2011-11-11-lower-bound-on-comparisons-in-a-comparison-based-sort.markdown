---
author: reddragon
comments: true
date: 2011-11-11 22:24:06+00:00
layout: post
slug: lower-bound-on-comparisons-in-a-comparison-based-sort
title: Lower bound on comparisons in a comparison-based sort
wordpress_id: 69
categories:
- Algorithms
- Sorting
---

I was asked this question recently. Here is a proof based on Information Theory.

Assume that we have to sort an array of n elements, all of which are distinct. Hence, there are $n! $ permutations possible, out of which only one is sorted.

Now let us assume the lower bound on the comparisons to be $f(n) $. Since each comparison has only 2 outcomes, thus,

$2^{f(n)} \geqslant n! $

has to hold. 

Therefore,

$f(n) = \log _2 ( n!)  $

which, by [Stirling's approximation](http://en.wikipedia.org/wiki/Stirling%27s_approximation) is $\Omega(n \log_2 n)$. Knuth also gives a similar explanation in Volume 3.
