---
author: reddragon
comments: true
date: 2012-09-16 20:55:56+00:00
layout: post
slug: profiling-in-python
title: Profiling in Python
wordpress_id: 228
---

I was trying to implement the Miller-Rabin algorithm for one of my home-works, in Python. I had already done this in C++ to solve [PON](http://www.spoj.pl/problems/PON/), but I wanted to try out Python, and see how fast I can get it to. I wrote a function to do 
$a\^b$ mod $n $
which used repeated squaring to get the result. However, the implementation wasn't fast enough. Dhruv suggested that I profile the code.

Here is how you profile a python script:
`python -m cProfile script.py`

And this is what I came to know

```
172 function calls (66 primitive calls) in 31.492 seconds
    
       Ordered by: standard name
    
       ncalls  tottime  percall  cumtime  percall filename:lineno(function)
            1    0.000    0.000    0.000    0.000 __future__.py:48(<module>)
            1    0.000    0.000    0.000    0.000 __future__.py:74(_Feature)
            7    0.000    0.000    0.000    0.000 __future__.py:75(__init__)
            1    0.020    0.020    0.020    0.020 hashlib.py:55(<module>)
            6    0.000    0.000    0.000    0.000 hashlib.py:94(__get_openssl_constructor)
            1    0.063    0.063   31.492   31.492 millerRabin.py:1(<module>)
        108/2   16.644    0.154   16.644    8.322 millerRabin.py:12(fastModularExp)
            2    0.008    0.004   16.672    8.336 millerRabin.py:21(millerRabin)
            1    0.000    0.000    0.000    0.000 os.py:743(urandom)
```

Note how the `fastModularExp()` function took a staggering 16 seconds. Now we came to know that the builtin [pow](http://docs.python.org/library/functions.html#pow) function in Python already does fast modular exponentiation. And since it is a part of a C library, it is quite fast. After doing this, I submitted it as a solution for [PON](http://www.spoj.pl/problems/PON/) and got accepted with 0.35 seconds, which was faster than my 0.90 submission with C++ :-)
