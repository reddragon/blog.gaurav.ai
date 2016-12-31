# Lock-Free Algorithms

* Memory Reorderings: http://preshing.com/20120515/memory-reordering-caught-in-the-act/
* C++ 11 has atomic ops. CAS: http://en.cppreference.com/w/cpp/atomic/atomic_compare_exchange
* Atomic / Volatile (in Java) to avoid reordering.
* https://www.kernel.org/pub/linux/kernel/people/paulmck/perfbook/perfbook.2011.01.02a.pdf has more intuition behind why reordering happens.
* There is compiler re-ordering which is visible in code-generated while compiling, but there can be processor re-ordering, which happens at run-time.
* Didn't understand some parts of this: http://preshing.com/20120710/memory-barriers-are-like-source-control-operations/

* [Jeff Preshing's blog post on lock-free Linear Search](http://preshing.com/20130529/a-lock-free-linear-search/).
* A bunch of lock-free algorithms are based on the Compare and Swap primitive. https://en.wikipedia.org/wiki/Compare-and-swap, which maps to the `cmpxchg` operation on x86.

* CAS is a Read-Modify-Write operation.

* Based on the Linear Search, we can implement a lock-free hash-table. We start from the index which maps to hash(key), and then probe from that point onwards to the first index which has 0.
