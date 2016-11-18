---
layout: post
title: "Sharding Databases: A quick trick"
date: 2016-11-16 23:26:28 -0800
comments: true
categories: 
---
One of the problems with serving databases is horizontal scalability (i.e., being able to add machines in the cluster), and load balance the read/write loads.

## Naive Solution
A naive way to rebalance traffic is to assign a part of the key-space to each machine. For an object $o$, with key $k$, the machine serving the object can be found out by $h$($k$) $\%$ $n$. Where $h$ is a hash-function, such as SHA or MD5. 

**Advantages**

- A simple function to compute where each key goes.

**Problems**

- $n$ is fixed, and the clients need to be informed when you update $n$.
- If you add/remove machines, you need to move all your existing data, so that the hash function works. If you have $K$ keys, you would incur $O$($K$) transfers.

## Consistent Hashing
<a href="https://en.wikipedia.org/wiki/Consistent_hashing" target="_blank">Consistent</a> <a href="https://www.youtube.com/watch?v=--4UgUPCuFM" target="_blank">Hashing</a> is an optimization on the naive solution, in that it avoids the need to copy the entire dataset. Each key is projected as a point on the edge of a unit circle. Every node in the cluster is assigned a point on the edge of the same circle. Then each key is served by the node closest to it on the circle's edge.

When a machine is added or removed from the cluster, each machine gives up / takes up a small number of keys. This rebalance happens in such a fashion that only $O$($\frac{K}{n}$) transfers happen. Where $n$ is the number of machines in the cluster.

**Advantages**

- Minimal number of data transfer between machines. Has been proven to be optimal.

**Problems**

* The clients need to know not just the number of nodes, but also the location of each node on the circle.
* Calculating which key goes to which machine, is slightly more comples, but still $O$(1).

Note that in both the above methods, when you are adding or removing machines, there is some amount of shutdown involved. In the first case, we need to completely turn-off reads and writes because the cluster is going through a complete rebalance. In the second case, we can just turn-off reads and writes for a fraction of the keyspace which is $\frac{1}{n}$ as compared to the first solution.


## Pinterest's Sharding Trick
Pinterest in it's <a href="https://engineering.pinterest.com/blog/sharding-pinterest-how-we-scaled-our-mysql-fleet" target="_blank">blogpost about MySQL sharding</a> talks about a setup where they use the key itself as a marker of which shard the key belongs to. When doing a write for the first time on the object $o$, we generate a key for it, in which we keep the higher $x$ bits reserved for the shard the object belongs to. The next time, there is a request for a read, we use those $x$ bits to find which shard should be queried.

Each shard is located on a certain machine, and the shard->machine map is kept in ZooKeeper (a good place to read & write small configs in a consistent fashion). Upon finding the shard, we lookup this map to locate the machine to which the request needs to be made.

When new machines are added, we simply create more shards, and start new writes start utilizing those new shards for populating the bits corresponding to the shards. This way, new writes and the reads correspodning to those writes dont hit the existing machines.

**Advantages**

* There is no copying whatsoever. Once you add new machines, they start receiving new data, provided you tell the system generating the keys about new machines.

**Disadvantages**

* Reads and writes are not balanced to begin with. Newer machines will start with 0 traffic, and slowly ramp up.
* There is an intermediary lookup involved for the shard->machine mapping.
* The key itself is modified. This might be okay for some setups, though.


## Sharding Trick Deux
Another trick that some setups apply is to have the key-space sufficiently pre-sharded to begin with. Then these shards are simply moved to other machines, if their current hosts can't serve them, as traffic increases. For MySQL, each shard is a separate database instance. We used a similar approach when operating HBase at FB, where we expected the need to add more machines in future.

