---
author: reddragon
comments: true
date: 2012-11-28 16:26:07+00:00
layout: post
slug: linking-c-templates
title: Linking C++ Templates
wordpress_id: 276
tags:
- c++
---

Today I was trying to link together code which uses C++ Templates. The usual accepted pattern is to put the declarations in the header, and the definitions in a separate .hpp / .cpp file. However, I was unable to get them to link it together.

To my surprise, I discovered (or re-discovered, probably) that, when dealing with C++ Templates, you need to put the definitions in the header file. A good explanation of why it is so, is [here](http://www.parashift.com/c++-faq-lite/templates-defn-vs-decl.html).
