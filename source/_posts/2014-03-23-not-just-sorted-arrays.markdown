---
layout: post
title: "Not-Just-Sorted-Arrays"
date: 2014-03-23 10:35:36 -0800
comments: true
categories: 
---
It is fascinating, how simple data structures can be used to build web-scale systems (Related: A funny video on <a href="https://www.youtube.com/watch?v=b2F-DItXtZs" target="_blank">MongoDB</a>). 
If this doesn't make sense to you yet, allow me to slowly build up to the story. One of the most simple, and yet powerful algorithm a programmer has in his toolbox is the <a href="http://en.wikipedia.org/wiki/Binary_search_algorithm" target="_blank">Binary Search</a>. There are far too many applications to it. Consider reading <a href="http://qr.ae/nSUuk" target="_blank">this Quora answer</a> for simple examples. I personally use it in <a href="https://www.kernel.org/pub/software/scm/git/docs/git-bisect.html" target="_blank">git bisect</a> to hunt down bad commits in a repository with tens of thousands of commits.

The humble sorted array is a beautiful thing. You can search over it in $O(\log n)$ time. There is one trouble though. You cannot modify it. I mean, you can, but then you will spoil the nice property of it being sorted, unless you pay an $O(n)$ cost to copy the array to a new location, and insert the new element. If you have reserved a large enough array before hand, you don't need to copy to a new array, but still have to shift elements and that will still be an $O(n)$ cost.

Also, if we were allowed to plot complexities on a graph, we can plot the insert complexity on the X-axis and search complexity on the Y-axis. Then all the suitable data-structures would hopefully be bound by the square with edges on <$O(1)$, $O(1)$> and <$O(n)$, $O(n)$>. The sorted array with <$O(n)$, $O(\log n)$> would lie somewhere on the bottom right corner, whereas, a simple unsorted array would be on the top-left with <$O(1)$, $O(n)$>. You can't do insertions better than $O(1)$ and you can't do searches better than $O(\log n)$ (although the bases and constants matter a lot, in practice).  

Now, how do we use a static structure, so that we retain the goodness of a sorted array, but allow ourselves the ability to add elements in an online fashion? What we have here, is a 'static' data-structure, and we are trying to use it for a 'dynamic' usecase. <a href="http://compgeom.cs.uiuc.edu/~jeffe/teaching/datastructures/notes/01-statictodynamic.pdf" target="_blank">Jeff Erickson's notes on Static to Dynamic Transformation</a> are of good use here. The notes present results related to how to use static data-structures to build dynamic ones. In this case, you compromise a bit on the search complexity, to get much better insert complexity.

The notes present inserts-only and inserts-with-deletions static to dynamic transformations. I haven't read the deletions part of it, but the inserts-only transformation is easy to follow. The first important result is: 

> If the static structure has a space complexity of $S(n)$, query complexity of $Q(n)$, and insert complexity of $P(n)$, then the space complexity of the dynamic structure would be $O(S(n))$, with query complexity of $O(\log n).Q(n)$, and insert complexity of $O(\log n).\frac{P(n)}{n}$ _amortized_.

Then the notes present the lazy-rebuilding method by Overmars and van Leeuwen. Which improves the first result's insertion complexity by getting the same complexity in the *worst case* instead of amortized. (Fun fact: <a href="http://en.wikipedia.org/wiki/Mark_Overmars" target="_blank">Overmars</a> is the same great fellow who wrote <a href="http://en.wikipedia.org/wiki/GameMaker:_Studio" target="_blank">Game Maker</a>, a simple game creating tool, which I used when I was 12! Man, the nostalgia :) I digress..)

The inserts-only dynamic structure, is pretty much how LSM trees work. The difference is the $L\_0$ array starts big (hundreds of MBs, or a GB in some cases), and resides in memory, so that inserts are fast. This $L\_0$ structure is later flushed to disk, but does not need to be immediately merged with a bigger file. That is done by background compaction threads, which run in a staggered fashion, so as to minimize disruption to the read workload. Read the <a href="http://research.google.com/archive/bigtable.html" target="_blank">BigTable</a> paper, to understand how simple sorted arrays sit at the core of the biggest databases in the world.

Next Up: Fractal Trees and others.
