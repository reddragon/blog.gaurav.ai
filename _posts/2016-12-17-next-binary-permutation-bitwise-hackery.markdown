---
layout: post
title: "Next Binary Permutation: Bitwise Hackery"
date: 2016-12-17 19:54:07 -0800
comments: true
categories:
---

Here is a puzzle that is fairly standard:

> Given an array of elements, find the lexicographically next permutation of that array.

As an example, if the array is [1, 2, 2, 3], the lexicographically next permutation would be [1, 3, 2, 2], followed by [3, 1, 2, 2] and so on. There is a <a href="https://www.nayuki.io/page/next-lexicographical-permutation-algorithm" target="_blank">really neat article</a> explaining how to solve this. If you don't know how to do it, I encourage you to try examples with array sized 4 and above, and try to see the patterns.

A recent problem I was solving was a variant of this.

> Given an unsigned integer, find the lexicographically next unsigned integer, with the same number of bits set.

It's trivial to observe that, we can reduce this problem to the above problem, as an array with just two kinds of elements, 0s and 1s.

Alright. Are we done? Not quite. The solution mentioned in the link is an $O(n)$ solution. Technically, an unsigned integer would be 32 or 64 bits. So $n$ would be one of those numbers for the purpose of the problem. It should be easy to repurpose the algorithm in the article mentioned above for our case. But I wanted to see if we can do it with as few operations as possible, because looping when operating with binary numbers is just not cool :-)

I chanced upon <a href="https://graphics.stanford.edu/~seander/bithacks.html#NextBitPermutation" target="_blank">Sean Anderson's amazing bitwise hacks page</a>, and I distinctly remember having seen this 7-8 years ago, when I was in Mumbai. Regardless, if you understand his solution: Awesome! It took me some time to figure out and I wrote a slightly slower but arguably easier to comprehend solution, which is 50% slower than his in my micro-benchmark, but better than the naive looping solution. So here goes.

## Example
Let's pick an example: $10011100$. The next permutation would be $10100011$.

As per the article above, we find the longest increasing suffix from right-to-left (called as longest non-increasing suffix from left-to-right in the article). In this case, it will be $11100$. Thus, the example is made of two parts: $100.11100$ ($.$ for separating).

The first zero before the suffix is the 'pivot', further breaking down the example: $10.0.11100$.

We swap the rightmost one in the suffix, with this pivot (rightmost successor in the article). So the example becomes $10.1.11000$. However, the suffix part needs to be sorted, since so far we were permuting with the prefix $10.0.$, but this is the first permuation with the prefix $10.1.$, and therefore the suffix should be it's own smallest permutation (basically, it should be sorted).

Hence, we move the zeroes in the suffix to the end, resulting in $10.1.00011$. This is the correct next permutation.

## Solution
```cpp
uint64_t next(uint64_t n) {
  // Find the first unset bit (pivot).
  uint64_t pivotBit = __builtin_ctz((n | n - 1) + 1);  

  // Set the first unset bit (pivot).
  uint64_t step1 = n | (1<<pivotBit);

  // Unset the first set bit (successor).
  uint64_t step2 = step1 & (step1 - 1);

  // Extract the part after the pivot.
  uint64_t suffixMask = (1 << pivotBit) - 1;
  uint64_t suffix = step2 & suffixMask;

  // Zero out the suffix, and only keep the 1's around.
  uint64_t final = (step2 & ~suffixMask) | (suffix >> __builtin_ctz(suffix));
  return final;
}
```

We'll break it down. Trust me, it's easier to grasp than the terse wisdom of Sean Anderson's snippet.

## Code-Walkthrough
```
// Find the first unset bit (pivot).
uint64_t pivotBit = __builtin_ctz((n | n - 1) + 1);
```
To find the pivot in the example $n = 10011100$, we set all the bits in the suffix to 1 first.

$n-1$ will set the trailing zeroes to 1, i.e., $10011011$, and $n \| n-1$ would result in a value with all original bits set, along with the trailing zeroes set to 1, i.e., $10011111$. Thus, all the bits in the suffix are now set.

 We now set the pivot bit to 1 (and unset the entire suffix), by adding 1. Using `__builtin_ctz` we can then find the number of trailing zeroes, which is the same as the bit number of the pivot. See the note below for `__builtin` functions.

```
// Set the first unset bit (pivot).
uint64_t step1 = n | (1<<pivotBit);
```

We then proceed to set the pivot. Since the value of $n$ was $10011100$, $step1 = 10111100$.

```
// Unset the first set bit (successor).
uint64_t step2 = step1 & (step1 - 1);
```

Now we need to unset the successor, which we can do by a trick similar to how we found the pivot. `step1 - 1` would unset the lowest significant set bit (the successor) and set all it's trailing zeroes (i.e., $10111011$). `step1 & (step1 - 1)` i.e., $10111100 \& 10111011$ would lead to zero-ing out of the successor bit and the trailing zeroes. Hence, $step2 = 10111000$.

```
// Extract the part after the pivot.
uint64_t suffixMask = (1 << pivotBit) - 1;
uint64_t suffix = step2 & suffixMask;
```

This is fairly straightforward, we extract the suffix mask, i.e., all the bits corresponding to the suffix part are set, and then $\&$ with the number $10.1.11000$ so far gives us the modified suffix, i.e. $11000$.

```
uint64_t final = (suffix >> __builtin_ctz(suffix)) | (step2 & ~suffixMask);
return final;
```

All we need to do now is to pull the 1s to the left in the suffix. This is done by left-shifting them by the number of trailing zeroes, so we get $00011$ (the first part of the calculation of `final`). This is our 'sorted' suffix we mentioned earlier.

Then we OR it with the number so far, but except the suffix part zero-ed out, so that we replace the unsorted suffix with this sorted suffix, i.e. $00011 \| 10100000 \implies 10100011$.

I hope this helped you breakdown what's going on, and probably served as a bridge between the naive solution and one-liner bitwise hacks.

Please leave any comments below. I'd be super happy to discuss any alternative solutions!

## Appendix: `__builtin` Functions
Whenever you are working with bitwise operations, gcc provides <a href="https://gcc.gnu.org/onlinedocs/gcc/Other-Builtins.html" target="_blank">built-in methods</a> such as `__builtin_popcount` (number of set bits in the argument), `__builtin_ctz` (number of trailing zeroes in the argument), and so on. These functions map to fast hardware instructions, and are also concise to write in code, so I use them whenever I can.
