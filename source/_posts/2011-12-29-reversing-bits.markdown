---
author: reddragon
comments: true
date: 2011-12-29 00:03:58+00:00
layout: post
slug: reversing-bits
title: Reversing Bits
wordpress_id: 108
categories:
- Algorithms
---

The problem is, Given a number of _n_ bits, reverse the bits. Normally, I would have used _2n_ bitwise operations to do this.

In CSE548, for a problem we reversed a string recursively, by reversing the two halves of the string, and then exchanging the positions of the two reversed halves. A string of bits, is a string after all.

So, we start with reversing the odd-even bits, then reversing pairs of bits, then reversing sets of 4 bits, and so on. So, this requires _3*log(n)_ bitwise operations, which is better. Here is an efficient implementation for reversing a 32-bit unsigned int.

[sourcecode lang="cpp"]
unsigned int reverse(unsigned int x)
{
    x = ((x & 0x55555555)<<1)  | ((x & 0xAAAAAAAA)>>1);
    x = ((x & 0x33333333)<<2)  | ((x & 0xCCCCCCCC)>>2);
    x = ((x & 0x0F0F0F0F)<<4)  | ((x & 0xF0F0F0F0)>>4);
    x = ((x & 0x00FF00FF)<<8)  | ((x & 0xFF00FF00)>>8);
    x = ((x & 0x0000FFFF)<<16) | ((x & 0xFFFF0000)>>16);
    return x;
}

void wrapper()
{
    cout << reverse(0xF00BAAF0);
}
[/sourcecode]
