---
layout: post
title: "Systems Design: Facebook TAO"
date: 2016-12-29 12:37:31 -0800
comments: true
categories:
---
TAO is a very important part of the infrastructure at Facebook. This is my attempt at summarizing the <a href="https://www.usenix.org/system/files/conference/atc13/atc13-bronson.pdf" target="_blank">TAO paper</a>, and the <a href="https://www.facebook.com/notes/facebook-engineering/tao-the-power-of-the-graph/10151525983993920/" target="_blank">blog post</a>, and the <a href="https://www.usenix.org/conference/atc13/technical-sessions/presentation/bronson" target="_blank">talk by Nathan Bronson</a>. I am purely referring to public domain materials for this post.

## Motivation
Memcache was being used as a cache for serving the FB graph, which is persisted on MySQL. Using Memcache along with MySQL as a look-aside/write-through cache makes it complicated for Product Engineers to write code modifying the graph while taking care of consistency, retries, etc. There has to be glue code to unify this, which can be buggy.

A new abstraction of Objects & Associations was created, which allowed expressing a lot of actions on FB as objects and their associations. Initially there seems to have been a PHP layer which deprecated direct access to MySQL for operations which fit this abstraction, while continuing to use Memcache and MySQL underneath the covers.

This PHP layer for the above model is not ideal, since:

1. Incremental Updates: For one-to-many associations, such as the association between a page and it's fans on FB, any incremental update to the fan list, would invalidate the entire list in the cache.

2. Distributed Control Logic: Control logic resides in fat clients. Which is always problematic.

3. Expensive Read After Write Consistency: Unclear to me.

## TAO

TAO is a write-through cache backed by MySQL.

TAO objects have a type ($otype$), along with a 64-bit globally unique id. Associations have a type ($atype$), and a creation timestamp. Two objects can have only one association of the same type. As an example, users can be Objects and their friendship can be represented as an association. TAO also provides the option to add inverse-assocs, when adding an assoc.

{% img center /images/2016/12/29/obj-assoc.png Objects-Assocs in TAO %}


### API
The TAO API is simple by design. Most are intuitive to understand.

* `assoc_add(id1, atype, id2, time, (k→v)*)`: Add an association of type `atype` from `id1` to `id2`.
* `assoc_delete(id1, atype, id2)`: Delete the association of type `atype` from `id1` to `id2`.
* `assoc_get(id1, atype, id2set, high?, low?)`: Returns assocs of `atype` between id1 and members of `id2set`, and creation time lies between $[high, low]$.
* `assoc_count(id1, atype)`: Number of assocs from `id1` of type `atype`.
* And a few others, refer to the paper.



As per the paper:
{% blockquote %}
TAO enforces a per-atype upper bound (typically 6,000) on the actual limit used for an association query.
{% endblockquote %}

This is also probably why the maximum number of friends you can have on FB is 5000.

## Architecture

There are two important factors in the TAO architecture design:

1. On FB the aggregate consumption of content (reads), is far more than the aggregate content creation (writes).
2. The TAO API is such that, to generate a newsfeed story (for example), the web-server will need to do the dependency resolution on its own, and hence will require multiple round-trips to the TAO backend. This further amplifies reads as compared to writes, bringing the read-write ratio to 500:1, as mentioned in Nathan's talk.

The choice of being okay with multiple round-trips to build a page, while wanting to ensure a snappy product experience, imposes the requirement that:

1. Each of these read requests should have a low read latency (cannot cross data-center boundaries for every request).
2. The read availability is required to be pretty high.

### Choice of Backing Store
The underlying DB is MySQL, and the TAO API is mapped to simple SQL queries. MySQL had been operated at FB for a long time, and internally backups, bulk imports, async replication etc. using MySQL was well understood. Also MySQL provides atomic write transactions, and few latency outliers.

### Sharding / Data Distribution
Objects and Associations are in different tables. Data is divided into logical shards. Each shard is served by a database.

Quoting from the paper:
{% blockquote %}
In practice, the number of shards far exceeds the number of servers; we tune the shard to server mapping to balance load across different hosts.
{% endblockquote %}

And it seems like the sharding trick <a href="http://blog.gaurav.im/2016/11/17/sharding-databases-a-quick-trick/" target="_blank">we credited to Pinterest</a> might have been used by FB first :-)
{% blockquote %}
Each object id contains an embedded shard id that identifies its hosting shard.
{% endblockquote %}

The above setup means that your shard id is pre-decided. An assoc is stored in the shard belonging to its `id1`.

### Consistency Semantics
TAO also requires "read-what-you-wrote" consistency semantics for writers, and eventual consistency otherwise.

### Leader-Follower Architecture
TAO is setup with multiple regions, and user requests hit the regions closest to them. The diagram below illustrates the caching architecture.
{% img center /images/2016/12/29/leader-follower.png TAO Leader-Follower Setup %}

There is one 'leader' region and several 'slave' regions. Each region has a complete copy of the databases. There is an ongoing async replication between leader to slave(s). In each region, there are a group of machines which are 'followers', where each individual group of followers, caches and completely serves read requests for the entire domain of the data. Clients are sticky to a specific group of followers.

In each region, there is a group of leaders, where there is one leader for each shard. Read requests are served by the followers, cache misses are forwarded to the leaders, which in turn return the result from either their cache, or query the DB.

Write requests are forwarded to the leader of that region. If the current region is a slave region, the request is forwarded to the leader of that shard in the master region.

The leader sends cache-refill/invalidation messages to its followers, and to the slave leader, if the leader belongs to the master region. These messages are idempotent.

The way this is setup, the reads can never be stale in the master leader region. Followers in the master region, slave leader and by extension slave followers might be stale as well. The authors mention an average replication lag of 1s between master and slave DBs, though they don't mention whether this is same-coast / cross-country / trans-atlantic replication.

When the leader fails, the reads go directly to the DB. The writes to the failed leader go through a random member in the leader tier.

### Read Availability
There are multiple places to read, which increases read-availability. If the follower that the client is talking to, dies, the client can talk to some other follower in the same region. If all followers are down, you can talk directly to the leader in the region. Following whose failure, the client contacts the DB in the current region or other followers / leaders in other regions.

{% img center /images/2016/12/29/read-availability.png Read Availability in TAO %}

### Performance
These are some client-side observed latency and hit-rate numbers in the paper.

{% img center /images/2016/12/29/tao-numbers.png Read Availability in TAO %}

The authors report a failure rate of $4.9 × 10^{−6}$, which is 5 9s! Though one caveat as mentioned in the paper is, because of the 'chained' nature of TAO requests, an initial failed request would imply the dependent requests would not be tried to begin with.

{% img center /images/2016/12/29/tao-summary.png %}

### Comments
* This again is a very readable paper relatively. I could understand most of it in 3 readings. It helped that there is a talk and a blog post about this. Makes the material easier to grasp.

* I liked that the system is designed to have a simple API, and foucses on making them as fast as they can. Complex operations have not been built into the API. Eventual consistency is fine for a lot of use cases,

* There is no transactional support, so if we have assocs and inverse assocs (for example `likes_page` and `page_liked_by` edges), and we would ideally want to remove both atomically. However, it is possible that assoc in one direction was removed, but there was a failure to remove the assoc in the other direction. These dangling pointers are removed by an async job as per the paper. So clients have to ensure that they are fine with this.

* From the Q&A after the talk, Nathan Bronson mentions that there exists a flag in the calls, which could be set to force a cache miss / stronger consistency guarantees. This could be specifically useful in certain use-cases such ash blocking / privacy settings.

* <a href="https://www.infoq.com/presentations/zen-pinterest-graph-storage-service" target="_blank">Pinterest's Zen</a> is inspired by TAO and implemented in Java. It powers messaging as well at Pinterest, interestingly (apart from the standard feed / graph based use-case), and is built on top of HBase, and a MySQL backend was in development in 2014. I have not gone through the talk, just cursorily seen the slides, but they seem to have been working on Compare-And-Swap style calls as well.
