---
author: reddragon
comments: true
date: 2012-01-29 02:20:36+00:00
layout: post
slug: hadoop-getting-my-hands-dirty
title: 'Hadoop: Getting My Hands Dirty'
wordpress_id: 119
categories:
- Advanced Project
tags:
- Hadoop
---

Those who are about to read this post, beware. Hadoop is a big beast. There are a lot of things churning inside. I am going to work on the Hadoop Scheduler this semester, so I will be dealing with it day-in and day-out. Having never used Hadoop, it took some time for me to get it up-and-running, and running some test code.

I am making some casual notes of how I went about it. It might help some of you in the future, hopefully, and will let me keep a ready-reference too.



	
  * The first step is to understand, what [Map Reduce](http://en.wikipedia.org/wiki/Map_Reduce), and [Hadoop](http://en.wikipedia.org/wiki/Hadoop) are. The Wiki pages for both are good-enough sources for the same.

	
  * Then, to actually set up Hadoop on Ubuntu, I used [this]( http://www.michael-noll.com/tutorials/running-hadoop-on-ubuntu-linux-single-node-cluster/) excellent tutorial. (Courtesy [Deepak](http://sundaycomputing.blogspot.com/)). The procedure should be slightly different for other distributions.

	
  * You might want to read [this](http://wiki.apache.org/hadoop/HadoopMapReduce) to understand how Hadoop can be used to implement Map Reduce jobs.

	
  * The Hadoop Wordcount [example](https://gist.github.com/1696581) is a good place to understand how a basic Map Reduce job is written in Hadoop. [This](http://hadoop.apache.org/common/docs/r0.20.2/mapred_tutorial.html#Example%3A+WordCount+v1.0) is the standard Hadoop documentation, which explains the example.However there are small changes in the API, and the documentation has not been updated to reflect that :-(. For example, `OutputCollector` has been replaced by the `Context` object in the Mapper and Reducer function prototypes. [Here](http://andrewhitchcock.org/?post=321) is a small summary. But mostly, you should be fine with the above-mentioned tutorial. Using the Wordcount example, I made a trivial modification to find the number of palindromes in a set of files. [Here](https://gist.github.com/1696587) is the code.


These are the sequence of steps I followed to get my job running:






	
  1. `$HADOOP_HOME/bin/hadoop/start-all.sh`

	
  2. `javac -classpath $HADOOP_HOME/hadoop-*-core.jar Palindrome.java`

	
  3. `jar -cvfe /path/for/jar/file/Palindrome.jar Palindrome Palindrome.class Palindrome\$PalindromeMapper.class Palindrome\$PalindromeReducer.class`

	
  4. `$HADOOP_HOME/bin/hadoop dfs -copyFromLocal /path/to/input /user/hadoop/input/path`

	
  5. `$HADOOP_HOME/bin/hadoop jar /path/for/jar/file/Palindrome.jar /user/hadoop/input/path /user/hadoop/output/path`

	
  6. `$HADOOP_HOME/bin/hadoop dfs -getmerge /user/hadoop/output/path /path/to/final/output`








	
  * Here are some of the common [Hadoop shell commands](http://hadoop.apache.org/common/docs/r0.17.1/hdfs_shell.html) that you might need. I used dfs, ls, cat, getmerge for running the Palindrome code.

	
  * I also read an example which deals with estimating the value of Pi. While there are [series](http://en.wikipedia.org/wiki/Leibniz_formula_for_pi), which help in finding the value iteratively, and can be parallelized by assigning the range of terms each node has to calculate, it can prove to be expensive. The reason being, each term needs to be calculated with arbitrary precision.The innovative method is to generate a large number of points within a unit square centered at the origin. If the number of points are large and randomly distributed, the ratio of the number of points inside the circle to the total points gives us the a good approximation of `PI/4`. We can parallize this by dividing the points based upon the quadrants / sectors they lie in, and summing up the respective counts. Note, here we need to do only one final arbitrary precision calculation.


