---
author: reddragon
comments: true
date: 2012-09-15 14:25:07+00:00
layout: post
slug: a-cool-way-to-look-at-symmetric-key-cryptography
title: A cool way to look at Symmetric Key Cryptography
wordpress_id: 223
categories:
- Classroom
tags:
- crypto
- insight
---

"Why encrypting twice with two symmetric keys using the same algorithm doesn't give you twice the security?" was the question that was asked in a recent CSE509 (System Security) class. I had the intuition that encrypting with the same algorithm twice with two different keys, K1 and K2, is essentially equivalent to encrypting with one key (say, K3). However, I didn't know how to convince others about this.

Someone pointed out that, since Symmetric Cryptography is essentially a combination of Permutation and Substitution at a very basic level (the person was referring to [P-Boxes](http://en.wikipedia.org/wiki/Permutation_box) and [S-Boxes](http://en.wikipedia.org/wiki/S-box), found in many algorithms), doing it twice is essentially equivalent to doing it once with some other key. 

I found that this was a more convincing argument (though very informal), about the security of the proposed mechanism.
