---
author: reddragon
comments: true
date: 2011-11-09 18:00:26+00:00
layout: post
slug: compendium-of-nice-algorithmic-observations
title: Compendium of Nice Algorithmic Observations
wordpress_id: 58
categories:
- Algorithms
---

Often we come across nice observations. I am going to write some of them here as and when I come across them.





  * A directed graph is acyclic if it has a valid topological sort. (By [Dhruv](http://dhruvbird.com))


  * The longest path can be found in a graph can be found by negating the weights of the edges, and then the length of the longest path is the absolute value of the shortest path in the new graph.


  * The shortest (and the longest) path in a Directed Acyclic Graph (DAG) can be found in linear time. (Hint: Topological Sort, Dynamic Programming) 


  * The longest path in a tree is the sum of the length of the two longest depth first searches from the root. 


