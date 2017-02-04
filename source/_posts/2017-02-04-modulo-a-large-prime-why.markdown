---
layout: post
title: "Modulo A Large Prime: Why?"
date: 2017-02-04 10:45:29 -0800
comments: true
categories:
---
The <a href="https://en.wikipedia.org/wiki/Rabin%E2%80%93Karp_algorithm" target="_blank">Karp-Rabin</a> algorithm for string matching (which is pretty elegant, and I strongly prefer it to KMP in most settings), uses the modulo operator when computing the hash of the strings. What is interesting is, it recommends using a prime number as the modulus for doing this.

Similarly, when computing which hash-table bucket a particular item goes to, the common way to do it is: $b = h(x)\bmod n$. Where $h(x)$ is the hash function output, $n$ is the number of buckets you have.

## Why do we need a prime modulus?
In hash functions, one should expect to receive pathological inputs. Assume, $n = 8$. What happens, if we receive $h(x)$ such as that they are all multiples of $4$? That is, $h(x)$ is in $[4, 8, 12, 16, 20, ...]$, which in $\bmod 8$ arithmetic will be $[4, 0, 4, 0, 4, ...]$. Clearly, only 2 buckets will be used, and the rest 6 buckets will be empty, if the input follows this pattern. There are several such examples.

As a generalization, if the greatest common factor of $h(x)$ and $n$ is $g$, then the number of buckets that will be used is $\large \frac{n}{g}$. This is easily workable on paper.

We ideally want to be able to use all the buckets. Hence, the number of buckets used, $\large \frac{n}{g}$ $= n$, which implies $g = 1$.

This means, the input and the modulus ($n$) should be co-prime (i.e., share no common factors). Given, we can't change the input, we can only change the modulus. So we should choose the modulus such that it is co-prime to the input.

For the co-prime requirement to hold for all inputs, $n$ has to be a prime. Now it will have no common factors with any input (except it's own multiples), and $g$ would be 1.

Therefore, we need the modulus to be prime in such settings. Let me know if I missed out on something, or my intuition here is incorrect.
