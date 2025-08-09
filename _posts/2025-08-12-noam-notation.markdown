---
layout: post
title: "'Noam Notation' for Readable Modeling Code"
date: 2025-08-12 12:08:37 -0700
comments: true
categories: transformer,
permalink: /:title/
---
Python typing allows us to specify the dimensions, but it doesn't specify what a particular dimension means.

<a href="https://scholar.google.com/citations?user=wsGvgA8AAAAJ&hl=en" target="_blank">Noam Shazeer</a> (of the Transformer, MoE, ... fame), came up with this notation that helps make the code slightly more readable at the first glance, but the benefits compound.

Consider a tensor `inputs`, it doesn't tell you much. If you enable string typing, Python will force you to specify that it is a Jax tensor of in the following manner: `inputs: jax.Array`. How about if the the tensor was named `inputs_BLD: jax.Array`. The `BLD` part signifies:

1. There are three dimensions.
2. The first is `B` (batch), second is `L` (length, or sequence), and the third and final one is `D` (or model).

These are what Noam calls 'Shape Suffixes' (more detail in <a href="https://medium.com/@NoamShazeer/shape-suffixes-good-coding-style-f836e72e24fd" target="_blank">his post here</a>).