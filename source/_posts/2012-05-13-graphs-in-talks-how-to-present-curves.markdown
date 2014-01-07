---
author: reddragon
comments: true
date: 2012-05-13 00:43:56+00:00
layout: post
slug: graphs-in-talks-how-to-present-curves
title: 'Graphs in Talks: How to present curves?'
wordpress_id: 204
categories:
- Algorithms
tags:
- talks
---

[Prof. Michael Bender](http://www.cs.sunysb.edu/~bender/) showed us a neat trick when presenting graphs in talks.

Often, we do experiments with Data-Structures and Algorithms, and we want to show that the cost of doing _blah_ with the _foo bar_ data structure, is $latex O(n)$ (which means that if we plot the actual cost against the value $latex n$, we should get a straight line).

Okay. What intuition do you have for something which costs $latex O(n\log{n})$. I would say its slope is somewhere between a line and a parabola. But how does the audience visually verify this instantly when seeing the graph?

On the y-axis, you do not plot the actual cost, but plot the ratio of the _actual cost to the value that you expected_, and show that the ratio is constant.

This is how we plotted something that we expected to be $latex O(n\log^2{n})$:

{% img /images/2012/05/moves.png %}

It was perfectly clear that the ratio is almost constant, and hence our hypothesis was correct.
