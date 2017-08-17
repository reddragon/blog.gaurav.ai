---
layout: post
title: "Dynamic Programming: You Can Do It Half Asleep!"
date: 2017-08-16 11:15:39 -0400
comments: true
categories: 
---
That was a click-baity title. :)

I wrote this post slightly geared towards interview practice, but it is also relevant otherwise.

But seriously, people make a big deal out of ‘Dynamic Programming’, in the light of programming interviews. The name is misleading, and for most problems in such interviews, you can go from a naive solution to an efficient solution, pretty easily. 

Any problem that has the following properties can be solved with Dynamic Programming:

1. Overlapping sub-problems: When you might need the solution to the sub-problems again.
2. Optimal substructure: Optimizing the sub-problems can help you get the optimal solution to the bigger problem.

You just have to do two things here:

1. Check if you can apply the above criteria.
2. Get a recursive solution to the problem.

That’s it. 

Usually the second part is harder. After that, it is like clockwork, and the steps remain the same almost all the time. 

**Example**

Assume, your recursive solution to say, compute the n-th fibonacci number, is:

$$F(n) = F(n - 1) + F(n - 2)$$

$$F(0) = F(1) = 1$$


**Step 1: Write this as a recursive solution first**

{% codeblock lang:cpp %}
int fib(int n) {
  if (n == 0 || n == 1) {
    return 1;
  } else {
    return fib(n-1) + fib(n-2);
  }
}
{% endcodeblock %}


Now, this is an exponential time solution. Most of the inefficiency comes in because we recompute the solutions again and again. Draw the recursion tree as an exercise, and convince yourself that this is true.

Also, when you do this, you at least get a naive solution out of the way. The interviewer at least knows that you can solve the problem (perhaps, not efficiently, yet).


**Step 2: Let’s just simply cache everything**

Store every value ever computed.

{% codeblock lang:cpp %}
int cache[20];
int fib(int n) {
  // Pre-fill all the values of cache as -1.
  memset(cache, -1, sizeof(cache)); 
  return fibDP(n);
}

int fibDP(int n) {
  // Check if we have already computed this value before.
  if (cache[n] != -1) {
    // Yes, we have. Return that.
    return cache[n];
  }
  
  // This part is just identical to the solution before.
  // Just make sure that we store the value in the cache after computing
  if (n == 0 || n == 1) {
    cache[n] = 1;
  } else {
    cache[n] = fibDP(n-1) + fibDP(n-2);
  }
  
  return cache[n]; 
}
{% endcodeblock %}

Let us compute how many _unique_ calls can we make to `fibDP`?

* There is one parameter, `n`.
* Hence, `n` unique values of `n` can be passed to fibDP.
* Hence, `n` unique calls.

Now, realize two things:

1. We would never compute the value of the function twice for the same value, ever. 
  - So, given $n$, we would call the function $n$ times, as seen above.
  - Each time with $O(1)$ work in each function call.
  - Total = $n$ calls with $O(1)$ work each => $O(n)$ total time complexity.


2. We are using up extra space.
  - We use as much extra space as:
  - Number of possible unique calls to the recursive function * space required for each value.
  - Since there are $n$ unique calls possible with an int value, space would be $O(n)$.
  - I have hard-coded a limit of 20 in my code. We can also use a Vector etc.

That’s it. We just optimized the recursive code from a $O(2^n)$ time complexity, $O(n)$ space complexity (recursive call stack space) to an $O(n)$ time, $O(n)$ space (recursive + extra space).

Example with a higher number of parameters

{% codeblock lang:cpp %}
int foo(int n, int m) {
  if (n <= 0 || m <= 0) {
   return 1;
  }
    
  return foo(n-1, m) + foo(n, m-1) + foo(n-1, m-1);
}
{% endcodeblock %}

Time complexity: $O(3^{n+m})$ [Work it out on paper, why this would be the complexity, if you are not sure.]


**DP Code**

{% codeblock lang:cpp %}
int cache[100][100];
int foo(int n, int m) {
  memset(cache, -1, sizeof(cache));
  return fooDP(n, m);
}

int fooDP(int n, int m) {
  if (n <= 0 || m <= 0) {
   return 1;
  }
  
  if (cache[n][m] == -1) {
    cache[n][m] = fooDP(n-1, m) + fooDP(n, m-1) + fooDP(n-1, m-1);
  }
  return cache[n][m];
}
{% endcodeblock %}

* Number of unique calls: $O(n* m)$
* Space Complexity: $O(n * m)$
* Time Complexity: $O(n * m)$

Assume I tweak foo and add an $O(n \log m)$ work inside each call, that would just be multiplied for the time complexity, i.e.,

Time complexity = O(unique calls) * O(work-per-call)

$$\implies O(n . m) \times O(n log m)$$

$$\implies O(n^2 m \log m)$$

$Space Complexity = O(unique calls) * O(space per call)

$$\implies O(n . m) \times O(1)$$

$$\implies O(n . m)$$


**Now just reinforce these ideas with this question**

 * Given a rectangular grid of size N x M,
 * What is the length of the longest path from bottom-left corner (0, 0) to top-right corner (N - 1, M - 1), assuming you can go up, right, diagonally?

**Extra Credit**

What we saw is called top-down DP, because we are taking a bigger problem, breaking it down into sub-problems and solving them first. This is basically recursion with memoization (we ‘memoize’ (fancy word for caching) the solutions of the sub-problems). 

When you absolutely, totally nail the recursive solution, some interviewers might want a solution without recursion. Or, probably want to optimize the space complexity even further (which is not often possible in the recursive case). In this case, we want a bottom-up DP, which is slightly complicated. It starts by solving the smallest problems iteratively, and builds the solution to bigger problems from that. 

Only if you have time, go in this area. Otherwise, even if you mention to the interviewer that you know there is something called bottom-up DP which can be used to do this iteratively, they should be at least somewhat okay. I did a short <a href="http://blog.gaurav.im/2011/07/20/longest-common-subsequence/" target="_blank">blog-post on converting a top-down DP to a bottom-up DP</a> if it sounds interesting.


