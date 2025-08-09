---
layout: post
title: "'Noam Notation' for Readable Modeling Code"
date: 2025-08-12 12:08:37 -0700
comments: true
categories: transformer,
permalink: /:title/
---
This post goes over what people on ML Twitter refer to as the 'Noam Notation', (named after <a href="https://scholar.google.com/citations?user=wsGvgA8AAAAJ&hl=en" target="_blank">Noam Shazeer</a>, of the Transformer, MoE, Multihead Attention, etc. fame). Noam himself calls the same thing 'Shape Suffixes' (more detail in <a href="https://medium.com/@NoamShazeer/shape-suffixes-good-coding-style-f836e72e24fd" target="_blank">his post here</a>).

Let's jump into it.

Consider a Jax (or PyTorch, etc.) tensor named `inputs`. The name itself doesn't tell you much. If you enable strict typing, Python will force you to specify that it is a Jax Array in the following manner: `inputs: jax.Array` when passing it or returning it from a function. 

Now, how about if the the tensor was named `inputs_BLD`, (when combined with typing `inputs_BLD: jax.Array`) where the `BLD` part additionally tells you that:

1. There are three dimensions.
2. The first is `B` (batch), second is `L` (length, or sequence), and the third and final one is `D` (or model).

Now if the convention is strictly followed, the code should pass the following check:

```python
assert inputs.shape == (batch_size, seq_len, d_model)
```

Where `batch_size`, `seq_len`, and `d_model` are your batch size, sequence length, and model dimension, respectively. Again, if your code strictly follows the notation, you would not need to actually perform the assertion.

Equipped with this invariant to all tensors in your code, you can easily tell that the following code is **guaranteed** to compile:

```python
query_BLHK = jnp.einsum('BLD,DHK->BLHK', inputs_BLD, w_q_DHK)
```

Here we do a matrix multiply between the `inputs_BLD` and the `w_q_DHK` tensors. `H` here stands for the number of heads, and `K` stands for the per-head embedding dimension. The exact meaning of those characters should either be easy to guess, or established somewhere in the code or documentation.

Regardless, it is easy to see that the two tensors in the above snippet should be compatible for matrix multiplication in that order, and the output tensor should be of shape [B, H, K]. That's a lot of useful information!

Now imagine if we suddenly turn off the notation. This is how the above snippet would look:

```python
query = jnp.einsum('BLD,DHK->BLHK', inputs, w_q)
```

Eww. Right? It's like we stripped a lot of useful information.

The readability benefits of this notation quickly compounds, especially in a large codebase. For example, see the <a href="https://github.com/google-deepmind/nanodo/blob/10aefdeed40a63293daf112b91a5538cd24fa3a4/nanodo/model.py#L121" target="_blank">NanoDO framework's implementation of Causal Attention</a> and other building blocks of the Transformer model. NanoDO uses the character `x` as a separator between dimensions (so `inputs_BLD` becomes `inputs_BxLxD`), but the motivation remains the same. Although one benefit of using a separator could be that you can use multiple characters to denote a dimension, since without a separator you are limited to 26 dimensions.

To summarize, a non-exhaustive list of what Noam Notation allows you to do is as follows:

1. Infer the semantics of a particular tensor just by reading its name.
2. Avoid compilation bugs.
3. Avoid silent bugs that do something unintentional such as broadcasting. 

The last one gives me the chills. It's much better to use Noam Notation than be sorry after wasting hours / days debugging why your model doesn't train *that* well. Give the Noam Notation a try the next time you are writing something from scratch. Let me know how you feel about this idea, or if you have your own neat ways of writing and organizing AI / ML related code.