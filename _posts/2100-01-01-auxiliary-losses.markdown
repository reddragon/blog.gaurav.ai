---
layout: post
title: "Efficient AI: Auxiliary Losses"
date: 2100-01-11 12:08:37 -0700
comments: true
categories: transformer,
permalink: /:title/
---
The <a href="https://arxiv.org/abs/1409.4842" target="_blank">Inception paper (Szegedy et al., 2015)</a> had a very neat trick hidden in plain sight, that very few people mention: Auxiliarly Losses. Let's quickly dive into what that is.

Many recent works are showing that the first few layers are doing the bulk of the heavy lifting when it comes to learning meaningful representations / minimizing the loss, etc. We can exploit this behavior by forcing the model to have an early-exit like behavior, and be depth-competitive.

What we mean by that in a non-scientific way is that:
> The first $l/2$ layers should get you say 90% of the performance. The next $l/4$ layers should get you 95% of the performance, and so on.

There is evidence that this is already the case. You can prune the last few layers, freeze the surviving layers, train a classification head on top.

There are a few ways to benefit from this behavior:

1. Have an early-exit like behavior: Just use the first few 
1. Force the model to have some sort of depth-competitive behavior

Let's assume that the model has $l$ layers, and the vanilla loss be denoted by $L$.

$$
L_0 = L_{\rm foo} + L_{\rm bar} + ...
$$

$$
L_\rm{total} = L_\rm{:l_2} + L_\rm{:l_4} + ...
$$