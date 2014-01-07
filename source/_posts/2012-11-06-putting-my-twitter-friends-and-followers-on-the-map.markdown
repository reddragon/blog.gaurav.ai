---
author: reddragon
comments: true
date: 2012-11-06 18:49:07+00:00
layout: post
slug: putting-my-twitter-friends-and-followers-on-the-map
title: Putting my Twitter friends and followers on the Map
wordpress_id: 219
tags:
- Random Hacks
---

I was quite impressed by the [Visualizing Friendships](https://www.facebook.com/notes/facebook-engineering/visualizing-friendships/469716398919) post on the Facebook Engineering blog. So I decided to try out some data visualization myself. Of course, I am no longer an intern at Facebook (I interned there this summer. A post coming up soon), so I don't have access to the millions of edges used in the map. So, I decided to do something similar for Twitter.

To plot anything I needed to find where my friends and followers were located. I used the Twitter API to find the list of my friends and followers. Then for each of the users, I found where they were located. This is not quite simple, since I want the location to be in the Latitude - Longitude format, and not everyone mentions their real locations in their Twitter profile.

The Twitter API had two basic problems:

1. It is slow
2. It places a lot of tight restrictions on how many results you can get at once.

But I waded through both of them, by (a) being patient (b) batching up requests in groups of size 100. This got me the public data about my friends whose profiles were publicly accessible. Now, a lot of them are living in places which might have multiple names, can be misspelled, do not accurately pinpoint the location of the person etc. For example, a friend who lives in Mumbai, can write 'Mumbai', 'Bombay' (the old name of Mumbai), 'Aamchi Mumbai' (a popular phrase, which translates to 'Our Mumbai'), or 'Maharashtra' (the state), etc. Thankfully, I found the [Yahoo! Placefinder API](http://developer.yahoo.com/geo/placefinder/), which solves this problem more or less. We can query for the lat-long pair of a place, and it will return its best guesses for the same.

Once I did that, I could use [R](http://www.students.ncl.ac.uk/keith.newman/r/maps-in-r) (thanks to [Aditya](https://github.com/truncs) for the suggestion) to plot the lat-long pairs on the World Map. The output isn't quite pleasing to the eye, but it does the job.

{% img center /images/2012/11/output.jpeg %}

You can find the script that gets the Lat-Long pairs [here](https://gist.github.com/3400704).

Edit: Since Yahoo! is commercializing their PlaceFinder API, I think the [Google GeoCoding API](https://developers.google.com/maps/documentation/geocoding/index) should be a suitable replacement. (Thanks to Dhruv for the suggestion).
