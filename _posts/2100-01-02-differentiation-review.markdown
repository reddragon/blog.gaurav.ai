---
layout: post
title: "Differentiation Review"
date: 2100-01-01 12:08:37 -0700
comments: true
categories: transformer,optimization
permalink: /:title/
---
This is a quick review of all things differentiation.

Consider a function $y = f(\mathbf{x})$, where $\mathbf{x} \sim (d)$ is a vector.

# Partial Derivative
The partial derivative of $f(\mathbf{x})$ w.r.t. $x_i$ is given by:

$$
\partial_{x_i} f(\mathbf{x}) = \frac{\partial f(y)}{\partial x_i} = \lim_{h \to 0}{\frac{f(\mathbf{x} + h\mathbf{e_i}) - f(\mathbf{x})}{h}}
$$

where $\mathbf{e_i}$

# Recap

1. What is a Jacobian?
xyz

1. What is a Hessian?
abc

1. What is the Chain Rule?
def

We will use this knowledge to later talk about automatic differentiation.