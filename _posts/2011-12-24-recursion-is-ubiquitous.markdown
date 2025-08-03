---
author: reddragon
comments: true
date: 2011-12-24 20:49:01+00:00
layout: post
slug: recursion-is-ubiquitous
title: Recursion is ubiquitous...
wordpress_id: 94
categories:
- Algorithms
---

... and so simple and elegant. In some sense, it is a piece of art, and one needs artists to appreciate it. I had this semi-non-trivial question in my mind:


> Print all the permutations of a given string S.


I had solved this before, but all I could recollect was that I had probably made it a little too dirty that time. The thing is, even with non-trivial problems, elegant solutions are possible with simple application of tools like Recursion / Divide & Conquer.

Prof. Bender asked us to visualize all the algorithmic techniques we learnt in CSE548 as 'tools in our toolbox'. Recursion / D&C is a very important tool IMHO.


> How do we break this problem into a smaller problem? 




Simple.

We only decide the character that will appear in the beginning of the permutation, and find all the permutations of the remaining string, and just stick the first character in front of each string.

When we have only one character left, the first character is the only permutation.

The code is as follows:

```cpp
string str;

void permute(int i)
{
  if(i == str.size()-1)
  {     
    cout << str << endl;
    return;     
  }     

  permute(i+1);
  for(int j = i+1; j < str.size(); j++)
  {
    swap(str[i], str[j]);
    permute(i+1);
    swap(str[i], str[j]);
  }

}

void wrapper()
{
  str = "abcd";
  sort(str.begin(), str.end());
  permute(0);
}
```

Isn't it beautiful? Its magical how we apparently do no work
in every step, and it all stitches together so beautifully.

