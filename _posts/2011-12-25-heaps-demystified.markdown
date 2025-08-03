---
author: reddragon
comments: true
date: 2011-12-25 22:57:26+00:00
layout: post
slug: heaps-demystified
title: Heaps Demystified
wordpress_id: 101
categories:
- Data Structures
---

I think the first time I learnt heaps was in an undergraduate course on Data Structures. Though I understood the basic idea, it was never crystal clear for me to code during a competition.

I took up the task of learning it afresh today. Here is a short gist.

A heap is a data structure that can be used to make fast (constant time) queries of the type 'what is the maximum element in the array', with fast updates (logarithmic time).

A heap is usually implemented as a balanced binary tree, but there are other variants like fibonacci heap, which I won't be discussing here. In the below discussion and code, I explain how I would implement a max-heap. For min-heaps, use the exact same techniques with small changes like flipping the comparison operators.

We need the following operations when implementing a heap:

* `topElem()`
* `insertElem(t)`
* `deleteTopElem(t)`

All the operations should be done in $O(\log{n})$ time.
Internally in a binary-heap, the root element is always atleast as big as both of its children, and this property of the heap exists recursively. (In min-heaps, root is as small, or smaller than both of its children)

It is easy to see that `topElem()` can be executed in constant time, since the maximum element would be at the root. (In min-heaps the minimum element would be at the root)

Now, when we need to remove the maximum (or the minimum element in min-heaps), we need to remove the root and preserve the heap property. Removing the root is simple, but what it leaves behind is not so trivial. Either the left, or the right child would be the biggest (or the smallest, in min-heaps) element left now. So, we compare the two. The bigger (or smaller. You get the idea now, I guess) of the two is placed in the root, leaving a void at the place where it existed. So, now we need to correct either the left, or the right sub-tree of the root, until the sub-tree is empty. This operation will be executed $O(\log{n})$ times, (costing $O(1)$ time, each time). So the complexity is $O(\log{n})$. Thus, we are done with `deleteTopElem()`.

`insertElem(t)` is even simpler, we place the new element in the lower-most level of the binary tree, where we have a place, or create a new level if we don't. Now, it is possible that the parent of the newly inserted element has lost the heap property. Thus, if the parent of the newly inserted element is greater than it, we swap the parent with the newly inserted element, and check if the new-parent has also lost the heap property. We continue this till we reach the root. This operation will be executed $O(\log{n})$ times, (costing $O(1)$ time, each time). So the complexity is $O(\log{n})$.

Here is a messy little implementation:

```cpp
template < class T >
class Heap
{
	std::vector<T> store;
	int capacity, used;

	void bubbleUp();
	void pushDown();

	public:
	Heap();

	void insertElem(T elem);
	T topElem();
	T deleteTopElem();
};

template< class T >
Heap< T >::Heap()
{
	capacity = 2;
	used = 1;
	store.resize(2);
}

template< class T >
void Heap< T >::insertElem(T elem)
{
	if(used == capacity)
	{
		capacity = (((capacity-1)<<1) + 1) + 1;
		store.resize(capacity);
	}
	store[used++] = elem;
	bubbleUp();
}

template<class T>
T Heap<T>::topElem()
{
	// There is no element in the heap.
	if(used - 1 == 0)
		return 0;

	return store[1];
}

template<class T>
void Heap<T>::bubbleUp()
{
	int ptr = used - 1;
	while(ptr != 1)
	{
		if(store[ptr] > store[ptr>>1])
		{
			swap(store[ptr], store[ptr>>1]);
			ptr >>= 1;
		}
		else break;
	}
}

template<class T>
T Heap<T>::deleteTopElem()
{
	// Empty heap
	if(used - 1 == 0)
		return 0;

	T ret = store[1];
	swap(store[1], store[used - 1]);
	used--;

	if(used - 1 > 0)
		pushDown();

	return ret;
}

template<class T>
void Heap<T>::pushDown()
{
	int ptr = 1;
	while(ptr < used)
	{
		if(ptr<<1 >= used) break;
		T left = store[ptr<<1];

		T right;
		bool right_branch = true;
		if ((ptr<<1) + 1 < used) right = store[(ptr<<1)+ 1];
		else right_branch = false;

		if(store[ptr] >= left && (!right_branch || store[ptr] >= right))
			break;

		if(left >= store[ptr])
		{
			if(!right_branch || left >= right)
			{
				swap(store[ptr], store[(ptr<<1)]);
				ptr = (ptr<<1);
				continue;
			}
			else
			{
				swap(store[ptr], store[(ptr<<1)+1]);
				ptr = (ptr<<1) + 1;
				continue;
			}
		}
		else if(!right_branch)
		{
			swap(store[ptr], store[(ptr<<1)+1]);
			ptr = (ptr<<1) + 1;
			continue;
		}
	}
}

void wrapper()
{
	Heap<int> h;
	int arr[] = { 4, 3, 7, 1, 10};

	for(int i = 0; i <  5; i++)
	{
		h.insertElem(arr[i]);
		cout << h.topElem() << endl;
	}
	cout << endl;
	for(int i = 4; i >=  0; i--)
	{
		cout << h.deleteTopElem() << endl;
	}

	Heap<string> s;
	string sarr[] = { "abc", "def", "ghi", "xyz", "zzz"};
	for(int i = 0; i <  5; i++)
	{
		s.insertElem(sarr[i]);
		cout << s.topElem() << endl;
	}
	cout << endl;
	for(int i = 4; i >=  0; i--)
	{
		cout << s.deleteTopElem() << endl;
	}
}
```

If you notice the code, I am inserting elements one by one, costing $O(\log{n})$ on each insert. And hence, $O(n\log{n})$ for $n$ elements. However, if we know the entire set of elements before hand, heap construction can be done in linear time, in a manner similar to `insertElem(t)`. Hint: Recursion.

You might also want to overload the comparison operators for custom data-structures.

I used [this presentation (ppt)](www.cis.upenn.edu/~matuszek/cit594-2008/Lectures/33-heapsort.ppt) to refresh my memory.
