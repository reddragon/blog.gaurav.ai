---
author: reddragon
comments: true
date: 2012-04-08 21:26:00+00:00
layout: post
slug: longest-palindromic-substring-in-linear-time
title: Longest Palindromic Substring in Linear Time
wordpress_id: 163
categories:
- Algorithms
---

We know that we can solve this problem using Suffix Arrays and Suffix Trees in Linear Time, but its not all that nice. I will probably like to implement the components of those some time. But there is a much nicer and simpler algorithm, called "Manacher's Algorithm" that I had known, but never bothered reading up on. Dhruv, today shared a link which explained it brilliantly. [Here](http://wcipeg.com/wiki/index.php?title=Longest_palindromic_substring#A_simple_asymptotically_optimal_solution) it is.

I will try to solve [NUMOFPAL](http://www.spoj.pl/problems/NUMOFPAL/) on SPOJ using Manacher's. I might also do [EPALIN](http://www.spoj.pl/problems/EPALIN/), which I already did earlier using an approach similar to Karp-Rabin.

**Update**: I solved [NUMOFPAL](http://www.spoj.pl/problems/NUMOFPAL/) using Manacher's.
