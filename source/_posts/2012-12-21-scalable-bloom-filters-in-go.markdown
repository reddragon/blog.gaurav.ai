---
author: reddragon
comments: true
date: 2012-12-21 01:41:25+00:00
layout: post
slug: scalable-bloom-filters-in-go
title: Scalable Bloom Filters in Go
wordpress_id: 278
categories:
- Data Structures
- Randomized Algorithms
---

I have been trying to learn some Go in my free time. While, I was trying to code up a simple [Bloom Filter](http://en.wikipedia.org/wiki/Bloom_filter), I realized that once a Bloom Filter gets too full (i.e., the [false positive rate](http://en.wikipedia.org/wiki/Bloom_filter#Probability_of_false_positives) becomes high), we cannot add more elements to it. We cannot simply resize this original Bloom Filter, since we would need to rehash all the elements which were inserted, and we obviously don't maintain that list of elements.

A solution to this is to create a new Bloom Filter of twice the size (or for that matter, any multiple >=2), and add new elements to the new filter. When we need to check if an element exists, we need to check in the old filter, as well as the new filter. If the new filter gets too full, we create another filter which is a constant factor (>=2) greater in size than the second filter. bit.ly uses a [solution](https://github.com/bitly/dablooms) similar to this (via Aditya).

We can see that if we have _N_ elements to insert in our 'Scalable' Bloom Filter, we would need _log N_ filters (base _r_, where _r_ is the multiple mentioned above). It is also easy to derive the cumulative false positive rate for this new Bloom Filter.

If the false positive rate of each of the individual constituent bloom filters is _f_, the probability that we do not get a false positive in one of the filters is (1-_f_).

Therefore the probability that we do not get a false positive in any of the q filters is, (1-_f_)^_q_.

Hence, the probability that we get a false positive in any of these q filters is:

1 - (1-_f_)^_q_.

Some rough estimates show that this cumulative false positive rate is around: _q_ * _f_ (only if _f_ is small). Where, _q_ is about log _N_, as we noted above. Therefore, if you have four filters, each with a false positive rate of 0.01, the cumulative false positive rate is about 4 * 0.01 = 0.04. This is exactly what we want.

What is beautiful in this construction is, the false positive rate is independent of how fast the filter sizes grow. If you maintain a good (small) false positive rate in each of the constituent filter, you can simply add up their false positive rates to get an estimate of the cumulative false positive rate (only if _f_ is small).

You can simply grow your filters fast (like around 5x), each time one filter becomes too full, so as to keep the number of filters small.

I have [implemented](https://github.com/reddragon/bloomfilter.go) this 'Scalable Bloom Filter' (along with the vanilla Bloom Filter and the Counting Bloom Filter) in Go. Please have a look, and share any feedback.
