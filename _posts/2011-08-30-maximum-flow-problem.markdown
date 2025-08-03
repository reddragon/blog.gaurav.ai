---
author: reddragon
comments: true
date: 2011-08-30 03:38:54+00:00
layout: post
slug: maximum-flow-problem
title: Maximum Flow Problem
wordpress_id: 7
---

The maximum flow is an optimization problem. You can read the background [here](http://en.wikipedia.org/wiki/Maximum_flow_problem).

I will discuss the code for a simple Ford-Fulkerson approach here.

There are three things that need to be true throughout the execution of the Ford-Fulkerson algorithm.

1. `c(u,v) >= f(u,v)`
This means that the flow between nodes `u` and `v` is never more than the capacity of the edge between `u` and `v`. This is the capacity constraint.

2. `f(u,v) = -f(v,u)`
This means that the net flow from `u` to `v` is opposite to the direction of net flow from v to u. This is the skew symmetry constraint.

3. Summation of `f(u,v)` for all pairs of `u` and `v` is `0`. This is the flow conservation constraint.

Now we need to find a path from source (`s`) to sink (`t`), so that it is possible to push to a positive flow on to that path. This means that for every pair of successive nodes, `u` and `v` on the path, `c(u,v) - f(u,v) > 0`.

This path is found using either [Breadth First Search](http://en.wikipedia.org/wiki/Breadth-first_search) or Depth First Search. I am listing the code below for augmenting path with [Depth First Search](http://en.wikipedia.org/wiki/Depth-first_search), since in BFS, there is a need for path-reconstruction.

Let's start with the basic initialization of the data-structures.
```cpp
#define MAXN 100
int adj[MAXN][MAXN], adjsz[MAXN],N;
int f[MAXN][MAXN],c[MAXN][MAXN],s,t;
bool g[MAXN][MAXN],vis[MAXN];

void init()
{
	for(int i=0;i<N;i++)
	{
		adjsz[i]=0;
		vis[i]=0;
		for(int j=0;j<N;j++)
			{ f[i][j]=0; c[i][j]=0; g[i][j]=0; }
	}
}
```
`MAXN` is the estimate of the number of nodes we are going to have. s is the source and t is the sink node. `adj[i]` is the adjacency list for node `i`, and `adjsz[i]` is the size of the adjacency list of node i. N is the total number of nodes. `c[u][v]` is the capacity of the edge between u and v, and similarly `f[u][v]` is the flow in the edge between u and v. `g[u][v]` is true if there is an edge between either `u` and `v`, or `v` and `u`. The vis array is a visited array, and `vis[i]` is marked true if it has been visited for finding the augmenting path.

Below is the code for adding a new edge between `u` and `v`.

```cpp
void add_edge(int u, int v, int cap)
{
	c[u][v]=cap;
	if(!g[u][v]) { adj[u][adjsz[u]++]=v; g[u][v]=1; }
	if(!g[v][u]) { adj[v][adjsz[v]++]=u; g[v][u]=1; }
}
```

Note that, if there is an edge from `u` to `v` with a positive capacity, we make sure that both `u` and `v` are in each others' adjacency list. This is done so that, if there is some flow between two nodes that needs to be cancelled to increase the total flow of the network, we can push a flow in the opposite direction on that edge.

Below is the code for Augmenting Path algorithm using DFS
```cpp
int augment_dfs(int u, int path_cap) 
{
	if(u==t) { return path_cap; }
	int v,cur_cap;
	vis[u]=1;
	for(int i=0;i<adjsz[u];i++)
	{
		v=adj[u][i];
		if(!vis[v] && (c[u][v]-f[u][v])>0)
		{
			cur_cap = min(path_cap,c[u][v]-f[u][v]);
			if(cur_cap <= 0) continue;
			vis[v]=1;
			int cap=augment_dfs(v,cur_cap);
			if(cap>0)
			{
				f[u][v]+=cap;
				f[v][u]-=cap;
				return cap;
			}
		}
	}
	return 0;
}
```
It is pretty easy to understand, it looks for neighbours of a node which are not visited and through which a positive flow can be pushed. It then determines exactly how much flow can be pushed through the current edge (between `u` and v). This value exists in the variable cur_cap. Then it recursively calls itself to repeat the procedure with `v`, and the new effective bottleneck capacity becoming `cur_cap`. When either the sink is found, or there is no eligible neighbor the recursion ends, and returns the current bottleneck capacity of the path, `path_cap`, if sink is found. If not, and there is no eligible neighbor, it returns `0`.

The returned values trickle down, and finally the ultimate bottleneck capacity is returned.

Ford-Fulkerson does nothing except trying to push more and more flow through the source by repetitively calling the `augment_dfs` function. When the returned value (bottleneck capacity of the augmented path) is `0`, it implies no more flow can be pushed.

```cpp
#define INF 1e7
int ford_fulkerson()
{
	int tot=0,cur=0;
	do 
	{ 
	  cur=augment_dfs(s,INF); 
	  if(cur<=0) break; 
	  tot+=cur;  
	  memset(vis,0,sizeof(vis)); 
	} while(cur>0);
	return tot;
}
```

In all we need to set N (the number of nodes), `s` (source), `t` (sink), and call the add_edge function for each edge we need to add. Also, set the `MAXN` macro appropriately.

Here is the complete code.
```cpp
#define MAXN 100
int adj[MAXN][MAXN], adjsz[MAXN],N;
int f[MAXN][MAXN],c[MAXN][MAXN],s,t;
bool g[MAXN][MAXN],vis[MAXN];

void init()
{
	for(int i=0;i<N;i++)
	{
		adjsz[i]=0;
		vis[i]=0;
		for(int j=0;j<N;j++)
			{ f[i][j]=0; c[i][j]=0; g[i][j]=0; }
	}
}

void add_edge(int u, int v, int cap)
{
	c[u][v]+=cap;
	if(!g[u][v]) { adj[u][adjsz[u]++]=v; g[u][v]=1; }
	if(!g[v][u]) { adj[v][adjsz[v]++]=u; g[v][u]=1; }
}

int augment_dfs(int u, int path_cap) 
{
	if(u==t) { return path_cap; }
	int v,cur_cap;
	vis[u]=1;
	for(int i=0;i<adjsz[u];i++)
	{
		v=adj[u][i];
		if(!vis[v] && (c[u][v]-f[u][v])>0)
		{
			cur_cap = min(path_cap,c[u][v]-f[u][v]);
			if(cur_cap <= 0) continue;
			vis[v]=1;
			int cap=augment_dfs(v,cur_cap);
			if(cap>0)
			{
				f[u][v]+=cap;
				f[v][u]-=cap;
				return cap;
			}
		}
	}
	return 0;
}

int augment(int u, int bottleneck)
{
	if(u==t) return bottleneck;
	vis[u]=1;
	
	for(int j=0;j<adjsz[u];j++)
	{
		int v=adj[u][j];
		if(vis[v]==1 || !(c[u][v]-f[u][v]>0)) continue;
		vis[v]=1;
		int cfp=augment(v,min(bottleneck,c[u][v]-f[u][v]));
		if(cfp==0) continue;
		f[u][v]+=cfp;
		f[v][u]-=cfp;
		return cfp;
	}
	return 0;
}

#define INF 1e7
int ford_fulkerson()
{
	int tot=0,cur=0;
	do 
	{ 
	  cur=augment_dfs(s,INF); 
	  if(cur<=0) break; 
	  tot+=cur;  
	  memset(vis,0,sizeof(vis)); 
	} while(cur>0);
	return tot;
}
```
