---
author: reddragon
comments: true
date: 2011-08-08 10:52:36+00:00
layout: post
slug: dealing-with-arbitrary-floating-point-operations
title: Dealing with Arbitrary Precision Floating Point operations
wordpress_id: 23
---

Another interesting problem I solved recently on SPOJ was [EVAL](https://www.spoj.pl/problems/EVAL/) (Digits of `e`). It is a challenge problem, and it involved printing the largest number of digits of e as possible (upto 1 million digits), within the time-limit of 25 seconds. (SPOJ processors are single core 733 MHz Pentium III processors AFAIK).

As far as I know, there is no way to actually find the digits, than using one of the series used for finding the value of e. One of the series is, [Taylor's series](http://en.wikipedia.org/wiki/Taylor_series).

`e(x) = 1 + (x/1!) + (x^2/2!) + (x^3/3!) + ..`

Thus, the value of `e`, can be calculated by substituting x=1. However, to obtain the value accurately upto 1 million digits is no small task. It requires arbitrary floating point ops.

Let me paint the picture better. The `M_PI` constant in C++ is correct upto 17 digits. Using Taylor's series and the long double datatype, you can get to only 19 digits.

I resorted to Python, and the its in-built bignum library using the Decimal module. Using the [Brother's series](http://mathworld.wolfram.com/e.html) expansion, the best I could get was a little more than 1000 digits, when using psyco.

{% codeblock e.py %}
import psyco
psyco.full()
from decimal import *
arr = {}
for i in range(1,240):
	arr[i]=2*i
getcontext().prec=1100
e = Decimal(2)
f = Decimal(1)
for i in range(1,240):
	a2=arr[i]
	f/=(a2)*(a2+1)
	e+=(f)*(a2+2);
print e
{% endcodeblock %}

Then, I switched to Ruby, and used the BigDecimal module to get nearly 30k digits in time.

{% codeblock e.rb %}
require 'bigdecimal'
require 'bigdecimal/math'
include BigMath
e = BigDecimal('1.0')
t = BigDecimal('1.0')
for i in 1..8400
  t=t.div(i,32000)
  e+=t
end
s = e.to_s
print "2."+s[3..-1]
{% endcodeblock %}

However, I think I can do much better in C++ if i have a good arbitrary-precision floating point operations library.

Any suggestions and pointers to better solutions are invited.
