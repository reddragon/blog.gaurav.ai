---
author: reddragon
comments: true
date: 2011-07-20 06:39:28+00:00
layout: post
slug: longest-common-subsequence
title: Longest Common Subsequence
wordpress_id: 9
tags:
- algorithms
- spoj
---

I was recently solving [Aibophobia](http://www.spoj.pl/problems/AIBOHP/) on the popular algorithm problem online judge, [SPOJ](http://www.spoj.pl).

The problem's solution involves finding the [Longest Common Subsequence](http://en.wikipedia.org/wiki/Longest_common_subsequence_problem) of two strings.

A trivial solution to the problem is exponential in complexity. However, [Dynamic Programming](http://en.wikipedia.org/wiki/Dynamic_programming) can be used to reduce the problem to time complexity $latex O(N^2)$.

There are usually two approaches to coding a Dynamic Programming solution. The first, is my favorite and very intuitive approach of Recursion with Memoisation, also known as the Top-down approach. 

{% codeblock topDownLCS.cpp %}
int dp[6100][6100];
int lcs(int i, int j)
{
	int &res=dp[i][j];
	if(res!=-1) return res;
	if(i==n) return res=0;
	if(j==m) return res=0;
	
	res=max(lcs(i+1,j),lcs(i,j+1));
	if(a[i]==b[j])
		return res=max(1+lcs(i+1,j+1),res);
	return res;
}
{% endcodeblock %}
Note that, here n, m are lengths of strings a and b, respectively and the dp array is initialized to -1. `lcs(i,j)` gives the value of the Longest Common Subsequence of strings a and b, starting from the i-th index of a and j-th index of b. Note that in lines 9-11 implement how the answer will be calculated recursively, and 6-7 define when the recursion will be terminated. Why is this fast? Because we _memoize_ the calculated values in the dp array and if `lcs(i,j)` is called again, the cached value would be returned. The LCS of two strings would be returned by the call `lcs(0,0)`.

Another approach is the bottom-up approach, which is easy to understand once you code the top-down approach. The problem with the previous top-down approach is that, in cases of large inputs, recursive calls, despite memoisation, might cause the solution to have a big constant. The bottom-up approach has the same $latex O(N^2)$ time complexity, but a lower constant.

My bottom-up approach to the problem was as follows:
{% codeblock bottomUpLCS1.cpp %}
int dp[6100][6100];
int lcs()
{
	for(int i=n-1;i>=0;i--)
	{
		for(int j=m-1;j>=0;j--)
		{
			dp[i][j]=max(dp[i+1][j],dp[i][j+1]);
			if(a[i]==b[j])
				dp[i][j]=max(dp[i][j],1+dp[i+1][j+1]);
		}
	}
	return dp[0][0];
}
{% endcodeblock %}
Note, the same problem is now done in the reverse fashion. The dp array needs to be initialized to be `0` only for all values of `dp[n][0]`, and `dp[0][m]`. 

However, there is one small optimization that can be done here. We do not need a 2D array for dp, since for `dp[i][j]`, it only needs the values of the `dp[i+1]` row, other rows are redundant. 

{% codeblock bottomUpLCS2.cpp %}
int dp[6100],prev[6100];
int lcs()
{
	for(int i=n-1;i>=0;i--)
	{
		for(int j=m-1;j>=0;j--)
		{
			dp[j]=max(prev[j],dp[j+1]);
			if(a[i]==b[j])
				dp[j]=max(dp[j],1+prev[j+1]);
		}
		memcpy(prev,dp,sizeof(int)*(m+1));
	}
	return dp[0];
}
{% endcodeblock %}
The above solution reduces the problem to space complexity of $latex O(N)$. In practice, reducing the space complexity improves the actual running time, since the small array fits more easily in the cache. 

Please refer the Dynamic Programming [tutorial on TopCoder](http://www.topcoder.com/tc?module=Static&d1=tutorials&d2=dynProg) to learn more.
