---
layout: post
title: "A gentle intro to libevent"
date: 2014-12-15 19:08:00 +0530
comments: true
categories: 
---
These past two days in some free time, I decided to explore this nifty C library called libevent. 

Following the theme from the previous post, the first question is: 'Why do we need it?'. If you are familiar with network programming, or any multithreaded programming which involves blocking IO, you already know the problem at hand. Right from the <a href="http://en.wikipedia.org/wiki/Direct_memory_access" target="_blank">hardware level</a> to the software level, a common problem that happens is: IO is slower than the CPU. If we have several tasks to finish, and the current task being executed is waiting for a blocking IO to finish, we should ideally work on the other tasks and let that blocking IO finish in the background, and check on it later.

When we have several such operations happening in the background, we need a way to figure out when a particular operation (such as read, write, accept a connection), can be performed without blocking, so that we can quickly do that, and return to other things. <a href="http://linux.die.net/man/2/select" target="_blank">select(2)</a>, poll(2), epoll(4), kqueue(2) (on \*BSD systems), are one of the several ways to do it. In essence, you register a set of file descriptors that you are interested in, and then call one of these 'backends'. They would usually block until either one of the fd-s that you are interested in, is ready for data to be read or written to it. If none of them is ready, it would block for a configured amount of time and then return.

The problem that libevent solves is, it provides an easy to use library for notifying when an event happens on the file descriptors which you consider interesting. It also hides the real backend (select, epoll, kqueue) being used, and this helps you avoid writing platform-dependent code (eg., kqueue works only on \*BSD) and if there were a new and improved backend in the future, your code would not change. It is like the JVM for asynchronous event notification system.

I only have experience with `select`, so my context is limited. Using `select` is very tedious. 
{% codeblock select.c %}
// Essentially a bitmask
fd_set readfds;

while (true) {
  // Zero out the bitmask
  FD_ZERO(&readfds);
  
  // Enable the fd that we are interested in
  FD_SET(sockfd, &readfds);

  int ret = select(sockfd + 1, &readfds, NULL, NULL, &timeout);
  if (ret < 0) {
    fprintf(stderr, "select() returned %d\n", ret);
  }
  
  // Is the bit corresponding to the fd enabled?
  // If yes, that fd is ready to be read from.
  if (FD_ISSET(sockfd, &readfds)) {
    // Do what we want here
  }
}
{% endcodeblock %}

In essence, what we do here is to create a set of file descriptors (`fd_set`). We then run a loop where every time we set all the file descriptors we are interested in, into that set. Then we call select(), and it either times out, or one of the bits in that set would be set. We have to check for each of the file descriptors. This makes it a little ugly. Other backends might be more pleasant to use, but libevent is way ahead of select in terms of usability. Here is some sample code:

{% codeblock libevent-1.cpp %}
event_base* eb = event_base_new();
event* t = event_new(eb, sockfd, EV_READ | EV_PERSIST, acceptConnCob, NULL);
event_add(t, NULL);
event_base_dispatch(eb);
{% endcodeblock %}

An `event_base` represents a single event loop like the one that we saw in the select example. To subscribe to changes in a file descriptor, we will first create an `event`. This can be done using `event_new`, which takes in the event base we created, the file descriptor, flags signalling when the event is active, the callback method and arguments to the callback method. In this particular example, we ask that the `acceptConnCob` method be called when the file descriptor is ready for reading (`EV_READ`) and persist this event, i.e, even when the event fires, automatically add it for the next time (`EV_PERSIST` is to be used here). Note that we had to add the file descriptors in every iteration of the while loop of the select example, so using the `EV_PERSIST` flag is a slight convenience here. Once, I have created the event, I need to add that event to the `event_base` it should be processed by, along with a timeout, using the `event_add` method. If the fd doesn't become active by the specified time, the callback will be called anyways. Finally, to get things running, we will 'dispatch' the event base, which will spawn a new thread to run the event loop.

Note that nowhere have I specified which backend to use. I don't need to. However, there are ways to prefer or avoid certain backends in libevent, using the `event_config` struct. Refer to the link in the end.

I can add multiple events, and there are a lot of options that you can use. For instance, I can create a timer by passing -1 as a file descriptor with the `EV_TIMEOUT` and `EV_PERSIST` flags, and the required timeout in `event_add`. This would call the timeout callback every 'timeout' seconds. Example:

{% codeblock libevent-2.cpp %}
event* e = event_new(eb, -1, EV_TIMEOUT | EV_PERSIST, pickFortuneCookieCob, NULL);
timeval twoSec = {2, 0};
event_add(e, &twoSec);
{% endcodeblock %}

I created a simple fortune cookie server (one of my favorite demo examples), where I have a set of messages, and if someone asks me for a fortune cookie, I will give them the current fortune cookie. Every few seconds, I will pick a new fortune cookie to be returned. This is implemented by having two events, one for accepting connections and the other for having a timer. The code is <a href="https://gist.github.com/reddragon/e8a706d527bb77822ab3" target="_blank">here</a>.

One small thing to keep in mind is that if the callbacks themselves to do something heavy, then it defeats the purpose of using libevent. This is because the callbacks are called from the same thread as the actual event loop. The longer the callback runs, the longer the event loop is not able to process other events. 

libevent allows you to do a lot of customizations. In the above example, I have added callbacks to override the logging mechanism, so that I can use glog (Google's logging library). There are several other features such buffered events and a lot of utility methods (such as <a href="http://www.wangafu.net/~nickm/libevent-2.0/doxygen/html/http_8h.html" target="_blank">creating simple http servers</a>), that you can find in the <a href="http://www.wangafu.net/~nickm/libevent-book/TOC.html" target="_blank">libevent book</a>.

There are other similar async event notification systems such as <a href="http://software.schmorp.de/pkg/libev.html" target="_blank">libev</a>, and <a href="https://github.com/libuv/libuv">libuv</a>, etc. but I haven't had the time to figure out the differences. I hope to cover the <a href="https://github.com/facebook/folly/blob/8d3b079a75fe1a8cf5811f290642b4f494f13822/folly/io/async/EventBaseManager.h">very interesting wrapper around libevent</a> in folly, Facebook's open source C++ library, in a future post.

