---
layout: post
title: "Make an amount N with C coins"
date: 2014-10-11 13:00:08 -0700
comments: true
categories: algorithms, dynamic-programmimg
---

This week we planned to discuss Dynamic Programming. The idea was to discuss about 4-5 problems, however, the very first problem kept us busy for an entire hour. The problem is a well known one: 'Given an infinite supply of a set of coin denominations, $C = {c\_1, c\_2, c\_3, ...}$, in how many ways can you make an amount N from those coins?'

The first question to be asked is, whether we allow permutations? That is, if, $c\_1 + c\_2 = N$, is one way, then do we count $c\_2 + c\_1 = N$, as another way? It makes sense to not allow permutations, and count them all as one. For example, if $N$ = 5, and $C$ = {1, 2, 5}, you can make 5 in the following ways: {1, 1, 1, 1, 1}, {1, 1, 1, 2}, {1, 2, 2}, {5}. 

We came up with a simple bottom-up DP. I have written a top-down DP here, since it will align better with the next iteration. The idea was, $f(N) = \sum f(N-c[i])$ for all valid $c[i]$, 
i.e., the number of ways you can construct $f(5) = f(5-1) + f(5-2) + f(5-5) \implies f(4) + f(3) + f(0)$. $f(0)$ is 1, because you can make $0$ in only one way, by not using any coins (there was a debate as to why $f(0)$ is not 0). With memoisation, this algorithm is $O(NC)$, with $O(N)$ space.

{% codeblock dp1.cpp %}
// table stores the results. All values are init to -1.
int table[MAXN];
// cval is the value of coins available.
int cval[MAXC];
// N is the amount, C is the number of coins.
int N, C;

int solve(int n) {
  int &res = table[n];
  if (res != -1) {
    return res;
  } else if (n == 0) {
    return res = 1;
  }
  
  res = 0;
  for (int i = 0; i < C; i++) {
    if (n - cval[i] >= 0) {
      res += solve(n - cval[i]);
    }
  }
  return res;
}
{% endcodeblock %}

This looks intuitive and correct, but unfortunately it is wrong. Hat tip to Vishwas for pointing out that the answers were wrong, or we would have moved to another problem. See if you can spot the problem before reading ahead.

The problem in the code is, we will count permutations multiple times, for example, for $n \= 3$, the result is 3 ({1, 1, 1}, {1, 2} and {2, 1}). {1, 2} and {2, 1} are being treated distinctly. This is not correct. A generic visualization follows.

Assume we start with an amount $n$. We have only two types of coins of worth $1$ and $2$ each. Now, notice, how the recursion tree would form. If we take the coin with denomination $1$ first and the one with denomination $2$ second, we get to a subtree with amount $n-3$, and on the other side, if we take $2$ first, and $1$ next, we get a subtree with the same amount. Both of these would be counted twice with the above solution, even though, the order of the coins does not matter.

{% img center /images/2014/10/duplicate-subtrees.jpg %}


After some discussion, we agreed on a top-down DP which keeps track of which coins to use, and avoids duplication. The idea is to always follow a lexicographic sequence when using the coins. It doesn't matter if the coins are sorted or not (actually yes, if you check all the coins that you are allowed to use, if they can be used). What matters is, always follow the same sequence. For example, if I have three coins {1, 2, 5}. Let's say, if I have used coin $i$, I can only use coins $[i, n]$ from now on. So, if I have used coin with value $2$, I can only use $2$ and $5$ in the next steps. The moment I use 5, I can't use 2 any more. 

If you follow, this will allow sequences of coins, in which the coin indices are monotonically increasing, i.e., we won't encounter a scenario such as {1, 2, 1}. This was done in a top-down DP as follows:

{% codeblock dp2.cpp %}
// This is a toy program, so please excuse the trivial flaws.
#define MAXN 2000
#define MAXC 20
// An N*C array, hard-coding the max N = 2000, C = 20.
int r[MAXN][MAXC];
int cval[MAXC];
int N, C;

/**
* O(N*C) solution.
* N is the sum to make, and C is the number of coins you can use. In the method
* n is the amount we have to make, and c denotes the coin number which is the
* smallest coin we can use, i.e., we can only use coins [Cc, Cn-1]. This is to
* prevent double counting.
*/
int solve(int n, int c) {
  int &res = r[n][c];

  if (res != -1) {
    return res;
  }

  if (n == 0) {
    return res = 1;
  }

  res = 0;
  for (int i = c; i < C; i++) {
    int rem = n - cval[i];
    if (rem >= 0) {
      res += f(rem, i);
    }
  }
  return res;
}

int solve(int n) {
  memset(r, -1, sizeof(r));
  return f(n, 0);
}
{% endcodeblock %}

Now, this is a fairly standard problem. I decided to check on the interwebs, if my DP skills have been rusty. I found the <a href="http://www.geeksforgeeks.org/dynamic-programming-set-7-coin-change/" targe="_blank">solution to the same problem on Geeks-for-Geeks</a>, where they present the solution in bottom-up DP fashion. There is also an $O(N)$ space solution in the end, which is very similar to our first faulty solution, with a key difference that the two loops are exchanged. That is we loop over coins in the outer-loop and loop over amount in the inner loop. 

{% codeblock dp3.cpp %}
int solve(int n) {
  int table[1000];
  memset(table, 0, sizeof(table));
  table[0] = 1;
  for (int i = 0; i < C; i++) {
    for (int j = cval[i]; j <= n; j++) {
      table[j] += table[j - cval[i]]; 
    }
  }
  return table[n];
}
{% endcodeblock %}

This is almost magical. Changing the order of the loops fixes the problem. I have worked out the table here step by step. Please let me know if there is a mistake.

Step 1: Calculating with 3 coins, uptil N = 10. Although we use an one-dimensional array, I have added multiple rows, to show how the values change over the iterations. 
{% img centre /images/2014/10/step-1.jpg %}

Step 2: Initialize table[0] = 1. 
{% img centre /images/2014/10/step-2.jpg %}

Step 3: Now, we start with coin 1. Only cell 0 has a value. We start filling in values for $n \= 1, 2, 3, ..$. Since, all of these can be made by adding \\$1 to the amount once less then that amount. Thus, the total number of ways right now, would be 1 for all, since we are using only the first coin, and the only way to construct an amount would be $1 + 1 + 1 + ... \= n$.
{% img centre /images/2014/10/step-3.jpg %}

Step 4: Now, we will use coin 2 with denomination \\$2. We will start with $n \= 2$, since we can't construct any amount less than \\$2 with this coin. Now, the number of ways for making amount \\$2 and \\$3 would be $2$. One would be the current number of ways, the other would be removing the last two $1$s, and adding a two. Similarily, mentally (or manually, on paper) verify how the answers would be.
{% img centre /images/2014/10/step-4.jpg %}

Step 5: We repeat the same for 3. The cells with a dark green bottom are the final values. All others would have been overwritten.
{% img centre /images/2014/10/step-5.jpg %}


I was looking into where exactly are we maintaining the monotonically increasing order that we wanted in the top-down DP in this solution. It is very subtle, and can be understood, if you verify step 4 on paper, for $4, 5, 6, ...$ and see the chains that they form. 

In the faulty solution, when we compute amounts in the outer loop, when we reach to amount $n$, we have computed all previous amounts for all possible coins. Now, if you compute from the previous solutions, they have included the counts for _all_ coins. If you try to calculate the count for $n$, using the coin $i$, and result for $n - cval[i]$, it is possible, that the result for $n - cval[i]$, includes the ways with coins > $i$. This is undesirable.

However, when we compute the other way round, we compute for each coin at a time, in that same lexicographical order. So, if we are using the results for $n - cval[i]$, we are sure, that it does not include the count for coins > $i$, because they haven't been computed yet, since they would only happen after computing the result for $i$.

As they say, sometimes being simple is the hardest thing to do. This was a simple problem, but it still taught me a lot.

