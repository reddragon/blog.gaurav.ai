---
author: reddragon
comments: true
date: 2012-05-07 02:21:53+00:00
layout: post
slug: closures-in-javascript
title: Closures in JavaScript
wordpress_id: 188
categories:
- JS
tags:
- nodejs
---

**Problem**: I need to maintain state for a function. In simpler and analogous terms, what static member variables do for a class, I want something to do the same for functions.


**Solution**: See the JavaScript code below:
[sourcecode lang="js"]
function foo() {
    var x = 0;
    return function () { return ++x; };
}
[/sourcecode]

I tried this in [nodejs](http://nodejs.org/), and here is the output:
`
> bar = foo()
[Function]
> bar()
1
> bar()
2
> bar()
3
`

The function `foo` returns a function which returns an incremented value of `x`. At first glance, to C/C++ programmers, this looks weird, because `x`, is a variable declared in `foo`, so how would the returned function have access to `x`?

Firstly, in JS, a variable continues to live, as long as there is a reference to it. So, as long as the returned function is referenced by someone, its copy of `x` is referenced, and it continues to live.

Secondly, what we are doing, is a concept called a [Closure](http://en.wikipedia.org/wiki/Closure_(computer_science)). 

Quoting the Wikipedia article verbatim here:



> A closure allows a function to access variables outside its immediate lexical scope. An upvalue is a free variable that has been bound (closed over) with a closure.



This is pretty clear. The upvalue here is `x`.



> The referencing environment binds the nonlocal names to the corresponding variables in scope at the time the closure is created, additionally extending their lifetime to at least as long as the lifetime of the closure itself. 



So, the copy of `x` that the function refers to, lives on.



> When the closure is entered at a later time, possibly from a different scope, the function is executed with its non-local variables referring to the ones captured by the closure.



This is what is happening when I execute the returned function.

This was an introductory post to Closures in JS, [here](http://howtonode.org/why-use-closure) is a much better and well-motivated post.

Again, the Nirvana is courtesy [Dhruv](http://dhruvbird.com) :-) 
