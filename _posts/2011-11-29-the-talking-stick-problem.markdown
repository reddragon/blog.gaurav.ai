---
author: Gaurav Menghani
comments: true
date: 2011-11-29 06:21:10+00:00
layout: post
slug: the-talking-stick-problem
title: The Talking Stick Problem
wordpress_id: 83
---

We have $N$ (>2) nodes, each synchronized amongst themselves and each of them has an identical program running on them. The program reads the incoming data on the network and generates some output, which is sent on the network. However, we want only one node to be transmitting this output at a time. If there is a failure, another node should pick up, but only one node should transmit the output until it fails. Upon a failure, regular operation should resume within $f$ ms.

An naive approach is to keep an arbitrator, who expects a ping from the node with a `talking stick' every ($f/4$) ms or so. If it does not, it assigns the talking stick to some-other node and resume operation. Whenever a node comes back up, it has lost its talking stick. A glaring weakness of this approach is its single point of failure. How do we solve this problem? We keep another node to make sure the arbitrator is alive. How do we know that the new node is alive? By keeping another node to see if the new node is alive all the time. And, Congratulations! We just landed ourselves an instance of the [Von Neumann Catastrophe](http://www.mindpowernews.com/SuperFreeWill.htm).

Let us look at this solution: We arrange the nodes in a ring. A is connected to B, B to C, C to D and so on. A is initially a node which begins talking. B knows A is the talking node, and expects a ping from A every $f/2$ ms or so. If A does not respond, B takes over the talking, and tells C to expect a ping from it in regular intervals. Looks better? Somewhat, but it ain't correct. If B fails, and then A fails, C should take over, but C thinks B is definitely not the primary, probably its A who is talking.

Another likely solution is this: Each node is assigned a unique numerical id, from 1 to $N$. Each node knows its own id, and we are given that the clocks are already synchronized amongst the nodes. The talking node, apart from the data, can transmit a ping to other nodes that it is alive. When a node $i$, which was the talking node, fails, all nodes realize this, since they stop receiving data from it on the network. Each node has a hard-coded timeout for $i$, after which they expect $i+1$ to take over. If $i+1$ is up and running it takes over and transmits on the network that it is alive and in-charge. If it is not, all nodes collectively time-out on $i+1$ and start expecting $i+2$ to take over now, and so on.

The above has a couple of shortcomings, firstly, the timeout for each node to take over might be small if $N$ is large. If the new node is supposed to take over in $f$ ms, the time-out for each node should not be more than $f/N$ ms. I am not sure if there might be problems synchronizing a large cluster of machines to such an accuracy. Second, if all nodes fail between $i$ and $i+101$, we wait for a 100 nodes even though they are dead.

I am still thinking of how to improve this further. Suggestions?
