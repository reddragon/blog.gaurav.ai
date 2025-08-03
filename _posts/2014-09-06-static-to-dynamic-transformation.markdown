---
layout: post
title: "Static to Dynamic Transformation - I"
date: 2014-09-06 12:56:30 -0700
comments: true
categories: 
---
Instead of going into fractal trees directly, I am going to be posting a lot of assorted related material that I am going through. Most of it is joint work with Dhruv and Bhuwan.

This post is about the <a href="http://web.engr.illinois.edu/~jeffe/teaching/datastructures/notes/01-statictodynamic.pdf" target="_blank">Static-to-Dynamic Transformation lecture by Jeff Erickson</a>. The motivation behind this exercise is to learn, how can we use a static data-structure, (which uses preprocessing to construct itself and answer queries in future) and create a dynamic data-structure that can continue taking inserts continuously.

I won't be formal here, so there would be a lot of chinks in the explanation. So either excuse me for that, or read the original notes.


## A Decomposable Search Problem
A search problem $Q$ with input $\mathcal{X}$ over data-set $\mathcal{D}$ is said to be decomposable, if, for any pair of disjoint data sets, $D$ and $D'$, the answer over $D \cup D'$, can be computed from the answers over $D$ and $D'$ in constant time. Or:

$Q(x, D \cup D') = Q(x, D) \diamond Q(x, D')$

Where $\diamond$ is an associative and commutative function which has the same range, as $Q$. Also, we should be able to compute $\diamond$ in $O(1)$ time. Examples of such a function would be $+$, $\times$, $min$, $max$, $\vee$, $\wedge$ etc. (but not $-$, $\div$, etc.). 

Examples of such a decomposable search problem can be a simple existence query, where $Q(x, D$ returns true if $x$ exists in $D$. Then the $\diamond$ function is the binary OR. Another example can be where the dataset is a collection of coordinates, and the query is the number of points which lie in a given rectangle. The $\diamond$ function here is $+$.

## Making it Dynamic (Insertions Only)
If we have a static structure that can store $n$ elements by needing $S(n)$ space, after $P(n)$ preprocessing, and can answer a query in $Q(n)$ time. What we mean by a _static_ data-structure is that we can only make inserts into the data-structure exactly once. But we can iterate through that data-structure (this is what the notes have missed, but is a requirement to get the bounds). 

Then, we can construct a dynamic data-structure the space requirement of the dynamic structure would be $O(S(n))$, with query time of $O(\log n).Q(n)$, and insert time of $O(\log n).\frac{P(n)}{n}$ _amortized_.

How do we do this? 

**Query**: Our data-structure has $l$ = $\lfloor{\lg{n}\rfloor}$ levels. Each level $i$ is either empty, or has a static-data structure with $2^i$ elements. Hence, since the search query is decomposable, the answer is simply $Q(D\_{0}) \diamond Q(D\_{1}) \diamond ... \diamond Q(D\_{l})$. It is easy to see why the total time taken for the query would be $O(\log n)$ Q(n). 

An interesting point is, if $Q(n) > n^\epsilon$, where $\epsilon > 0$ (which essentially means, if $Q(n)$ is polynomial in $n$), then the total query time is $O(Q(n))$. So, for example, if $Q(n) = n^2$, with the static data-structure, the query time with the dynamic data-structure would be $O(Q(n))$. Here is the proof, the total query time is: $\sum{Q(\frac{n}{2^i})} \implies \sum{(\frac{n}{2^i})^\epsilon} \implies n^\epsilon \sum{(\frac{1}{2^i})^\epsilon} \implies n^\epsilon . c \implies O(n^\epsilon) \implies O(Q(n))$ .


**Insert**: For insertion, we find the smallest empty level $k$, and build $L\_k$ with all the preceding levels ($L\_0$, $L\_1$, ..., $L\_k$) and the new element, and discard the preceding levels. Since it costs $P(n)$ to build a level, and each element will participate in the array building process $O(\log n)$ times (or jump levels that many times), we will pay the $P(n)$ cost $O(\log n)$ times. Over $n$ elements, that is $O(\log n).\frac{P(n)}{n}$ per element _amortized_. Again, if $P(n) > n^{1+\epsilon}$ for any $\epsilon > 0$, the amortized insertion time per element is $(O(P(n)/n)$. The proof is similar to what we described above for the query time.

**Interesting Tidbit**
Recollect what we mean when we say that a data-structure is _static_. A Bloom Filter is a static data-structure in a different way. You can keep inserting elements into it dynamically up to a certain threshold, but you can't iterate on those elements. 

The strategy to make it dynamic is very similar, we start with a reasonably sized bloom-filter, keep inserting into it as long as we can. Once it is too full, we allocate another bloom-filter of twice the size, and insert elements into that, from now on. And so on. The queries are done on all the bloom-filters and are a union of their individual results. An implementation is <a href="https://github.com/reddragon/bloomfilter.go" target="_blank">here</a>.

**What Next**: Deamortization of this data-structure with insertions as well as deletions. Then we will move on to Cache-Oblivious Lookahead Arrays, Fractional Cascading, and eventually Fractal Trees. This is like a rabbit hole!
