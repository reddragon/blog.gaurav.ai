---
author: reddragon
comments: true
date: 2012-02-14 03:28:31+00:00
layout: post
slug: miscellaneous-project-research-worthy-ideas-wip
title: Miscellaneous Project / Research Worthy Ideas [WIP]
wordpress_id: 138
categories:
- Algorithms
- Data Structures
---

I would scribble some project / research - worthy ideas. That may or may not yield much benefit, but I would probably like to travel down that path some time.

- Concurrent Linked Lists
  Linked Lists that can be operated on concurrently. There has been some work done on Lock-Free Linked Lists etc, probably worth checking out, and implementing.

- Bloom Filters / Quotient Filters
  Definitely worth implementing an efficient Bloom Filter / Quotient Filter. An exciting research area is to design a Bloom-Filter type data structure to efficiently answer the query - "Is there an element in the range [p,q]?", with a NO (which is guaranteed), or MAYBE (the false-positive rate should be adjustable).

- Persistent / Temporal Data Structures
  See Prof. Erik Demaine's [lecture](http://courses.csail.mit.edu/6.851/spring12/lectures/L01.html).

- Sorting / Searching
  Practical In-Place Merge-Sort [[PS]](www.diku.dk/~jyrki/Paper/mergesort_NJC.ps)

- Dynamic RMQ / LCA in O(1) time. 
  Simplify what Cole and Hariharan did for LCA in [this](http://citeseer.uark.edu:8080/citeseerx/viewdoc/summary?doi=10.1.1.105.3441) paper. And/or devise a dynamic RMQ mechanism which can be done in O(log n) / O(1).

- Fractional Cascading
  This is a really cool idea. Read about it [here](http://blog.ezyang.com/2012/03/you-could-have-invented-fractional-cascading/). It helps speed up bounded-box queries by a log factor.


Please feel free to suggest ideas.
