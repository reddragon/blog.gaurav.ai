---
layout: post
title: "'Noam Notation' for Readable Modeling Code"
date: 2025-08-12 12:08:37 -0700
comments: true
categories: transformer,
permalink: /:title/
---
This post goes over what people on ML Twitter call this the 'Noam Notation', (named after <a href="https://scholar.google.com/citations?user=wsGvgA8AAAAJ&hl=en" target="_blank">Noam Shazeer</a>, of the Transformer, MoE, Multihead Attention, etc. fame). Noam himself calls this 'Shape Suffixes' (more detail in <a href="https://medium.com/@NoamShazeer/shape-suffixes-good-coding-style-f836e72e24fd" target="_blank">his post here</a>). Let's jump into it.

Consider a Jax (or PyTorch, or whatever) tensor named `inputs`. The name itself doesn't tell you much. If you enable strict typing, Python will force you to specify that it is a Jax Array of in the following manner: `inputs: jax.Array` when passing it or returning it from a function. 

Now, how about if the the tensor was named `inputs_BLD`, (when combined with typing `inputs_BLD: jax.Array`) where the `BLD` part additionally tells you that:

1. There are three dimensions.
2. The first is `B` (batch), second is `L` (length, or sequence), and the third and final one is `D` (or model).

Now if the naming is accurate and respected in the code, the code should pass the following check:

```python
assert inputs.shape == (batch_size, seq_len, d_model)
```

Where `batch_size`, `seq_len`, and `d_model` are your batch size, sequence length, and model dimension, respectively. Again, if your code actually follows the notation, you would not need to actually perform the assertion.

Equipped with this information, you can easily tell that the following code will also likely compile:

```python
query = jnp.einsum('BLD,DHK->BLHK', inputs_BLD, w_query_DHQ)
```

The readability benefits of this notation quickly compounds! Concretely, a non-exhaustive list of what Noam's Notation allows you to do is:

1. Infer the semantics of a particular tensor just by reading its name.
2. Avoid compilation bugs.
3. Avoid silent bugs that do something unintentional such as broadcasting. 

The last one gives me the chills, so it's much better to use Noam's Notation than be sorry later. Give it a try the next time you are writing something from scratch.