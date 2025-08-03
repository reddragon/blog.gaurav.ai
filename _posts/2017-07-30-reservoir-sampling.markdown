---
layout: post
title: "Back to Basics: Reservoir Sampling"
date: 2017-07-30 10:06:42 -0700
comments: true
categories: 
---
If you have a dataset that is either too large to fit in memory, or new data is being added to it on an ongoing basis (effetively we don't know its size), there will be the need to have algorithms, which have a:

1. Space Complexity that is independent of the size of the dataset, and, 
2. Time Complexity per item of the dataset that is either constant, or otherwise is very small. 

Examples of such datasets could be clicks on Google.com, friend requests on Facebook.com, etc.

One simple problem that could be posed with such datasets is: 

> Pick a random element from the given dataset, ensuring that the likelihood of picking any element is the same. 

Of course, it is trivial to solve if we know the size of your dataset. We can simply pick a random number in $(0, n\-1)$ ($n$ being the size of your dataset). And index to that element in your dataset. That is of course not possible with a stream, where we don't know $n$.

Reservoir Sampling does this pretty elegantly for a stream $S$:

```
sample, len := null, 0
while !(S.Done()):
  x := S.Next()
  len = len + 1
  if (Rand(len) == 0):
    sample = x
return sample
```

The idea is simple. Every new element you encounter, replace your current choice with this new element with a probability of $\large\frac{1}{l}$. Where $l$ is the total length of the stream (including this element), encountered so far. When the stream ends, you return the element that you had picked at the end.

However, we need to make sure that the probability of each element being picked is the same. Let's do a rough sketch:

1. When the length of the stream is $1$, the probability of the first element being picked is $1.0$ (trivial to check this).
2. Assuming that if this idea works for a stream of size $l$, we can prove that it works for a stream of size $l+1$. 
  - Since it holds for a stream of size $l$, all elements before the $l+1$-th element have the same likelihood, i.e., $\large\frac{1}{l}$.
  - The new element will replace the selected element with a probability of $\large\frac{1}{l+1}$, but the existing element will remain with a probability of $\large\frac{l}{l+1}$.
  - Hence the probability of each of the elements seen so far being selected will be, $\large\frac{1}{l} . \large\frac{l}{l+1} = \large\frac{1}{l+1}$.
  - The probability of the new element being selected, as we stated earlier is $\large\frac{1}{l+1}$.
  - Hence, the probability will be the same for all the elements, assuming it holds for a stream of size $l$.
3. Given that the property holds for $n = 1$, and (2) is true, we can prove by induction that this property holds for all $n \gt 1$.  

There could be a weighted variant of this problem. Where, each element has an associated weight with it. At the end, the probability of an item $i$ being selected should be $\large\frac{w_i}{W}$. Where, $w_i$ is the weight of the $i$-th element, and $W$ is the sum of the weights of all the elements.

It is straight-forward to extend our algorithm to respect the weights of the elements:

1. Instead of `len`, keep `W`.
2. Increment `W` by $w_i$ instead of just incrementing it by 1.
3. The new element replaces the existing element with a probability of $\large\frac{w_i}{W}$.

In a manner similar to the proof above, we can show that this algorithm will also respect the condition that we imposed on it. Infact the previous algorithm is a special case of this one, with all $w_i = 1$.

Credits:

[1] Jeff Erickson's <a href="https://courses.engr.illinois.edu/cs473/sp2017/notes/06-bloom.pdf" target="_blank">notes on streaming algorithms</a> for the general idea about streaming algorithms.
