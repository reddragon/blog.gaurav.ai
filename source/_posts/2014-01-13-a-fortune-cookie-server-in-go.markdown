---
layout: post
title: "A fortune cookie server in Go"
date: 2014-01-13 11:17:10 +0530
comments: true
categories: golang hacking
---
I really like the concept of [Fortune Cookies in *nix systems](http://en.wikipedia.org/wiki/Fortune_(Unix)), and I absolutely love the Hindi movie [Andaz Apna Apna](http://www.imdb.com/title/tt0109117/). So, I thought I would write up a simple fortune-cookie server which serves random quotes from the movie. A lot of my friends liked it.

So, I thought it will be even nicer if I could generalize it, and add a bunch of other movies and TV serials, that are popular. So I wrote up [Elixir](https://github.com/reddragon/elixir), which is a generic fortune-cookie server written in Go. This new fortune-cookie server was hosted on [rand(quotes)](http://randquotes.com), and had quotes from movies like [Quentin Tarantino's movies](http://www.imdb.com/name/nm0000233/), [Lord of the Rings](http://en.wikipedia.org/wiki/The_Lord_of_the_Rings_(film_series)), and the popular TV shows [Breaking Bad](http://www.imdb.com/title/tt0903747/), and [Game of Thrones](http://www.imdb.com/title/tt0944947/). 

Using Elixir, it is extremely simple to write a fortune-cookie server which serves quotes from multiple quote databases. All you need to do is create the a file that contains the quotes you want to serve, one per line, and give it a name like `foo.quotes`. Place it in the directory where the server was started from, and those quotes would be serve from the `/foo` endpoint. 

To make it more fun, `/foo?f=cowsay` returns the quote in the [cowsay](http://en.wikipedia.org/wiki/Cowsay) format! Something like this

```
 _________________________________________
/ Walter White: If you don’t know who I   \
| am, maybe your best course would be to  |
\ tread lightly.                          /
 -----------------------------------------
        \   ^__^
         \  (oo)\_______
            (__)\       )\/\
                ||----w |
                ||     ||

``` 

You can create many such quotes databases, and also add/delete/modify them while the server is running, and the server will pick up the changes. 

A full-featured fortune-cookie server would look something like this:
{% codeblock server.go %}
package main

import (
	"flag"
	"github.com/reddragon/elixir"
)

func main() {
	listenPort := flag.Int("port", 80,
		"The HTTP port to listen on (default: 80)")
	flag.Parse()
	elixir.Start(*listenPort)
}
{% endcodeblock %}

_Implementation Note_: To implement the feature of keeping tab on the quote databases, without having to restart the server, one way was to use the [Inotify subsystem](http://en.wikipedia.org/wiki/Inotify) in Linux, [using Go](http://golang.org/pkg/syscall/#InotifyInit). But this didn't work for OSX. So I wrote up a quick and dirty implementation which does ```ioutil.ReadDir(".")``` periodically, and filters all the files which have a ```.quotes``` extension.
