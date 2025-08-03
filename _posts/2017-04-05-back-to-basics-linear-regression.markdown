---
layout: post
title: "Back to Basics: Linear Regression"
date: 2017-04-05 14:06:40 +0530
comments: true
categories:
---
Taking inspiration from <a href="http://www.allthingsdistributed.com/" target="_blank">Werner Vogel's 'Back to Basics' blogposts</a>, here is one of my own posts about fundamental topics. While on a long-haul flight with no internet connectivity, having exhausted the books on my kindle, and hardly any inflight-entertainment, I decided to code up Linear Regression in Python. Let's look at both the theory and implementation of the same.

## Theory

Essentially, in Linear Regression, we try to estimate a dependent variable $y$, using independent variables $x_1$, $x_2$, $x_3$, $...$, using a linear model.

More formally, 

$$y = b + W_1 x_1 + W_2 x_2 + ... + W_n x_n + \epsilon$$

Where, $W$ is the weight vector, $b$ is the bias term, and $\epsilon$ is the noise in the data.

It can be used when there is a linear relationship between the input $X$ (input vector containing all the $x_i$, and $y$).

One example could be, given a vending machine's sales of different kind of soda, predict the total profit made. Let's say there are three kinds of soda, and for each can of that variety sold, the profit is 0.25, 0.15 and 0.20 respectively. Also, we know that there will be a fixed cost in terms of electricity and maintenance for the machine, this will be our bias, and it will be negative. Let's say it is $100. Hence, our profit will be:

$$y = -100 + 0.25x_1 + 0.15x_2 + 0.20x_3$$

The problem is usually the inverse of the above example. Given the profits made by the vending machine, and sales of different kinds of soda (i.e., several pairs of $(X_i, y_i)$), find the above equation. Which would mean being able to find $b$, and $W$. There is a closed-form solution for Linear Regression, but it is expensive to compute, especially when the number of variables is large (10s of thousands).

Generally in Machine Learning the following approach is taken for similar problems:

1. Make a guess for the parameters ($b$ and $W$ in our case).
2. Compute some sort of a loss function. Which tells you how far you are from the ideal state.
3. Find how much you should tweak your parameters to reduce your loss.

**Step 1**
The first step is fairly easy, we just pick a random $W$ and $b$. Let's say $\theta = (W, b)$, then $h_\theta(X_i) = b + X_i.W$. Given an $X_i$, our prediction would be $h_\theta(X_i)$.

**Step 2**
For the second step, one loss function could be, the average absolute difference between the prediction and the real output. This is called the 'L1 norm'.

$$L_1 = \frac{1}{n}\sum_{i=1}^{n} \text{abs}(h_\theta(X_i) - y_i)$$

L1 norm is pretty good, but for our case, we will use the average of the squared difference between the prediction and the real output. This is called the 'L2 norm', and is <a href ="http://www.chioka.in/differences-between-the-l1-norm-and-the-l2-norm-least-absolute-deviations-and-least-squares/" target="_blank">usually preferred over L1</a>.

$$L_2 = \frac{1}{2n}\sum_{i=1}^{n} (h_\theta(X_i) - y_i)^2$$

**Step 3** We have two sets of params $b$ and $W$. Ideally, we want $L_2$ to be 0. But that would depend on the choices of these params. Initially the params are randomly chosen, but we need to tweak them so that we can minimize $L_2$.

For this, we follow the <a href="https://en.wikipedia.org/wiki/Stochastic_gradient_descent" target="_blank">Stochastic Gradient Descent algorithm</a>. We will compute 'partial derivatives' / gradient of $L_2$ with respect to each of the parameters. This will tell us the slope of the function, and using this gradient, we can adjust these params to reduce the value of the method.

Again,

$L\_2 = \frac{1}{2n}\sum\_{i=1}^{n} (h\_\theta(X\_i) - y\_i)^2$.

Deriving w.r.t. $b$ and applying chain rule,

$\large \frac{\partial L}{\partial b}$ = $2 . \large\frac{1}{2n}$ $\sum\_{i=1}^{n} (h\_\theta(X\_i) - y\_i) . 1$ (Since, $\frac{\partial (h\_\theta(X\_i) - y\_i)}{\partial b} = 1$)

$ \implies \large \frac{\partial L}{\partial b}$ $= \sum\_{i=1}^{n} (h\_\theta(X\_i) - y\_i)$

Similarly, deriving w.r.t. $W\_j$ and applying chain rule,

$\large \frac{\partial L}{\partial W\_j}$ = $\large\frac{1}{n}$ $\sum\_{i=1}^{n} (h\_\theta(X\_i) - y\_i) . X\_{ij}$

Hence, at each iteration, the updates we will perform will be,

$b = b - \eta \large\frac{\partial L}{\partial b}$, and,
$W\_j = W\_j - \eta \large\frac{\partial L}{\partial W\_j}$.

Where, $\eta$ is what is called the 'learning rate', which dictates how big of an update we will make. If we choose this to be to be small, we would make very small updates. If we set it to be a large value, then we might skip over the local minima. There are a lot of variants of SGD with different tweaks around how we make the above updates.


Eventually we should converge to a value of $L_2$, where the gradients will be nearly 0.

## Implementation

The complete implementation with dummy data in about 100 lines is <a href="https://gist.github.com/reddragon/91c023a123b8aab4c200183173e583fc" target="_blank">here</a>. A short walkthrough is below.

The only two libraries that we use are `numpy` (for vector operations) and `matplotlib` (for plotting losses). We generate random data without any noise.

```py
def linear_sum(X, W, b):
    return X.dot(W) + b

def data_gen(num_rows, num_feats, op_gen_fn=linear_sum):
    data = {}
    W = 0.1 * np.random.randn(num_feats)
    b = 0.1 * np.random.randn()
    data['X'] = np.random.randn(num_rows, num_feats)
    data['y'] = op_gen_fn(data['X'], W, b)
    return data
```

Where `num_rows` is $n$ as used in the above notation, and `num_feats` is the number of variables. We define the class `LinearRegression`, where we initialize `W` and `b` randomly initially. Also, the `predict` method computes $h_\theta(X)$.

```py
class LinearRegression(object):
    def __init__(self):
        self.W = None
        self.b = 0

    def init_matrix(self, X):
        self.W = 0.1 * np.random.randn(X.shape[1])
        self.b = 0.1 * np.random.randn()

    def predict(self, X):
        if self.W is None:
            self.init_matrix(X)

        return X.dot(self.W) + self.b
```

The crux of the code is in the `train` method, where we compute the gradients.

```py
def train(self, data, iters, lr):
        X = data['X']
        y = data['y']

        orig_pred = self.predict(X)
        orig_l1 = self.l1_loss(orig_pred, y)
        orig_l2 = self.l2_loss(orig_pred, y)

        l1 = orig_l1
        l2 = orig_l2

        l1_losses = []
        l2_losses = []
        l1_losses.append(l1)
        l2_losses.append(l2)

        for it in range(iters):
            pred = self.predict(X)

            # Computing gradients
            s1 = (pred - y)
            s2 = np.multiply(X, np.repeat(s1, X.shape[1])\
                    .reshape(X.shape[0], X.shape[1]))
            wGrad = np.sum(s2, axis=0) / X.shape[0]
            bGrad = np.sum(s1) * 1.0 / X.shape[0]

            # Updates to W and b
            wDelta = -lr * wGrad
            bDelta = -lr * bGrad
            self.W += wDelta
            self.b += bDelta

            l1 = self.l1_loss(pred, y)
            l2 = self.l2_loss(pred, y)

            l1_losses.append(l1)
            l2_losses.append(l2)

        print 'Original L1 loss: %Lf, L2 loss: %Lf ' % (orig_l1, orig_l2)
        print 'Final L1 loss: %Lf, L2 loss: %Lf' % (l1, l2)
```

For the given input, with the fixed seed and five input variables, the solution as per the code is:

```
- b:  -0.081910978042
- W:  [-0.04354505  0.00196225 -0.2143796   0.1617485  -0.17349839]
```

This is how the $L_2$ loss converges over number of iterations:

<!-- center -->
![600 600 Convergence of L2 loss]({{ site.baseurl }}/assets/img/2017/04/05/linear_reg.png)

To verify that this is actually correct, I serialized the input to a CSV file and used R to solve this.

```
> df <- read.delim(file="lin_reg_data", header=F, sep=",")
> lm(df[,1] ~ df[,2]+df[,3]+df[,4]+df[,5]+df[,6])

Call:
lm(formula = df[, 1] ~ df[, 2] + df[, 3] + df[, 4] + df[, 5] +
    df[, 6])

Coefficients:
(Intercept)      df[, 2]      df[, 3]      df[, 4]      df[, 5]      df[, 6]
  -0.084175    -0.041676    -0.005627    -0.213620     0.164027    -0.179344
```

The `intercept` is same as $b$, and the rest five outputs are the $W_i$, and are similar to what my code found.
