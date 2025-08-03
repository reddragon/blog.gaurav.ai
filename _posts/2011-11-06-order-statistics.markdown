---
author: reddragon
comments: true
date: 2011-11-06 04:54:28+00:00
layout: post
slug: order-statistics
title: Order Statistics
wordpress_id: 37
categories:
- Algorithms
- Randomized Algorithms
- Sorting
tags:
- sorting
---

How do you find the kth biggest element in an array of size n?

A naive $O(n\log{n})$ method would be to sort the array and return the element arr[n-k]. But we are looking for something linear in the length of the array.

Now, this comes from one of the CSE548 lectures of [Prof. Michael A. Bender](http://www.cs.sunysb.edu/~bender/).

Let us look at a Randomized Algorithm approach to this:
`
Randomly pick a pivot p

Partition the elements into the left sub-array with elements <= p and right sub-array with elements > p respectively.

If rank(p) = k, then return p

If rank(p) > k, then return the k th element from the left sub-array

If rank(p) < k, then return the k-rank(p) th element from the right sub-array 
`

This definitely smells like $O(n\^2)$. But turns out, in the average case it is not.

If you assume that your pivots are all good, and there is a 1/2 probability of choosing a good pivot (your pivot has a rank between n/4 and 3n/4, inclusive), your recurrence relation is only as bad as this,
$T(n) = T(3n/4) + O(n) $

Which is, $T(n) = \theta(n)$.

Surprisingly this can be done deterministically. [An 'All-Stars' deterministic algorithm devised by Blum, Floyd, Pratt, Rivest, Tarjan](ftp://reports.stanford.edu/www/pub/public_html/public_html/cstr.old/reports/cs/tr/73/349/CS-TR-73-349.pdf), does this in $O(n) $. I haven't read it yet though. 

One of the new tools that Prof. Bender hands you in CSE548, is the notion of Randomized Algorithms, which work 'with high probability'. I will probably go deeper in that field later.
