---
author: reddragon
comments: true
date: 2012-11-25 05:22:32+00:00
layout: post
slug: five-awesome-shell-utilities-you-might-not-know-about
title: Five Awesome Shell Utilities You Might Not Know About
wordpress_id: 264
tags:
- Random Hacks
---

**pgrep**
I always used to do "ps -ax | awk '/procname{print $1}'", until I learnt that, we could simply do "pgrep procname", and it will list the PIDs of all the processes with  in their names.

**pkill**
Similarly, I used to do "ps -ax | awk '/procname{print $1}' | xargs kill". As you must have guessed, this kills all the processes with names having 'procname' in them. But, a much simpler way is to just do "pkill procname"

**zcat** (and other related utilities)
A lot of times, we need to grep through an archive. For this, we usually copy the archive somewhere else, grep on the resulting files, and then delete these files. zcat is much simpler, in the sense that, it uncompresses an archive and displays the result on the standard output. Now you can pipe the output to grep. Or, you can directly use zgrep! See some other related utilities [here](http://www.thegeekstuff.com/2009/05/zcat-zless-zgrep-zdiff-zcmp-zmore-gzip-file-operations-on-the-compressed-files/).

**netcat**
[netcat](http://netcat.sourceforge.net/) is a damn neat networking utility, which reads and writes data across the network using TCP. This is pretty nifty because we can pipe the output of a command to a process running on a different machine. This is extremely useful for monitoring. Thanks to Dhruv for introducing this one.

**strace**
This utility can be used to print the list of systems calls (along with their arguments), being made by a program while it is running. How cool is that! See the output of 'strace ls' [here](https://gist.github.com/4142492).
