---
author: reddragon
comments: true
date: 2013-01-25 13:31:04+00:00
layout: post
slug: putting-my-twitter-friends-and-followers-on-the-map-ii-using-d3-js
title: Putting my Twitter friends and followers on the Map - II (Using D3.js)
wordpress_id: 284
categories:
- JS
---

I had [done a visualisation using R](/2012/11/07/putting-my-twitter-friends-and-followers-on-the-map/), where I plotted the locations of my friends and followers on Twitter on a map. I re-did this visualisation using [D3.js](http://d3js.org/). It is a fantastic visualisation tool, which a lot of features. I could only explore a fraction of the API for my purpose, but you can see a lot of cool [examples](https://github.com/mbostock/d3/wiki/Gallery) on their page.

The final output was something like this (a better look [here](http://bl.ocks.org/4623023)):

{% img /images/2013/01/Screen-Shot-2013-01-25-at-6.52.54-PM1.png %}

I wanted to resize the bubbles when there are a lot of points in the vicinity, but I'll leave that for later.

You can have a look at the [D3.js code](https://gist.github.com/4623023), and the [python script](https://gist.github.com/4634169) which gets the lat-long pairs using the Twitter API, and the Google GeoCoding API (Yahoo! decided to commercialize their GeoCoding API sadly).

(The map data and some inspiration for the code, is from [here](http://markmarkoh.com/blog/d3-dot-js-animated-map-visualization/))
