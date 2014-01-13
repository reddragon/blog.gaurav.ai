---
layout: post
title: "More writing this year"
date: 2014-01-13 11:08:44 +0530
comments: true
categories: general
---
It has almost been a year since I wrote something. For the most part, I have been too busy to share something. Since the past one year, I have been working on [HBase at Facebook](https://www.facebook.com/UsingHbase), which is the backbone of Facebook Messages, and many other important services at Facebook. Also, I've moved to [Mountain View, California](http://en.wikipedia.org/wiki/Mountain_View,_California), and I absolutely love the surroundings. 

I have been trying my hand at different things, like learning some ML, Go, trying to learn how to play an Electric Guitar, and other things. One thing I want to follow this year would be to continue doing new things, and keep sharing my experiences.

Finally, I have also ditched WordPress in favor of [Octopress](https://github.com/imathis/octopress), a Markdown-style blogging framework built on top of [Jekyll](http://jekyllrb.com/). What this means is, I just need to worry about the content, which I can write in simple Markdown format. Octopress generates a completely static website for me to use. I don't have to setup the Apache-MySQL monstrosity to serve a simple blog. 

However, the transition isn't _very_ smooth.
 
* I had to get my posts from WordPress into a Markdown format. For this, I used [exitwp](https://github.com/thomasf/exitwp). 
* I had to copy the images I had uploaded to my WP setup to my Octopress sources directory, and manually change the image tags to point to the right location in all the markdown files.
* For LaTeX, I am using [MathJax](http://www.mathjax.org/) [with Octopress](http://www.idryman.org/blog/2012/03/10/writing-math-equations-on-octopress/). I have only lost two things in this transition:
* Obviously, I lost the ability to receive comments natively, and lost the older comments on my posts. This is fine by me, since I don't receive too many comments anyways. I will enable Disqus on the blog for future comments.
* Also, WP has this ridiculous URL scheme for posts, which is something like `yourblog.com/?p=XYZ`, where `XYZ` is a number, while Octopress has a more sensible, `:year/:month/:date/:title` scheme. Google had indexed my blog according to the older scheme and now, and anybody who has linked to a specific blog post, will now be redirected to the main page. In short, its not pleasant.

However, the big win is that it is super-easy for me to write posts and host a blog. Earlier, this blog was put up on a free shared hosting site, and it was very clumsy to manage my blog. And as of the time of writing this post, I am hosting multiple blogs on a very lightweight VPS, and as long as I don't get DDoS-ed, this machine is more than capable of hosting several such static-only blogs. Because, after all, how hard is it to serve static HTML :)

I have a lot to share about what I learnt in the last year, so keep looking :)
