---
layout: post
title: "A Gentle Intro to PyTorch"
date: 2017-04-23 21:40:55 -0700
comments: true
categories:
---
<a href="http://pytorch.org/" target="_blank">PyTorch</a> is a fairly new deep-learning framework released by Facebook, which reminds me of the JS framework frenzy. But having played around with PyTorch a slight bit, it already feels fun.

To keep things short, I liked it because:

1. Unlike TensorFlow it allows me to easily print Tensors on the screen (no seriously, this is a big deal for me since I usually take several iterations to get a DL implementation right).
2. TensorFlow adds a layer between Python and TensorFlow. TensorFlow even has it's own variable scope. This is way too much abstraction, that I don't appreciate for my experimental interests.
3. Interop with numpy is easy in PyTorch, with the simple `.numpy()` suffix to convert a Tensor to a numpy array.
4. Unlike Torch, it is not in Lua (also doesn't need the LuaRocks package manager).
5. Unlike Caffe2, I don't have to write C++ code and write build scripts.

PyTorch's website has a <a href="http://pytorch.org/tutorials/beginner/deep_learning_60min_blitz.html" target="_blank">60 min. blitz tutorial</a>, which is laid out pretty well.

Here is the summary to get you started on PyTorch:

* `torch.Tensor` is your `np.array` (the NumPy array). `torch.Tensor(3,4)` will create a `Tensor` of shape (3,4).
* All the functions are pretty standard. Such as `torch.rand` can be used to generate random Tensors.
* Indexing in Tensors is pretty similar to NumPy as well.
* `.numpy()` allows converting Tensor to a numpy array.
* For the purpose of a compute graph, PyTorch lets you create `Variable`s which are similar to `placeholder` in TF.
* Creating a compute graph and computing the gradient is pretty easy (and automatic).

This is all it takes to compute the gradient, where `x` is a variable:

{% codeblock lang:py %}
x = Variable(torch.ones(2, 2), requires_grad=True)
y = x + 2
z = y * y * 3
out = z.mean()

out.backward()
print(x.grad)
{% endcodeblock %}

Doing backprop simply with the `backward` method call on the scalar `out`, computes gradients all the way to `x`. This is amazing!

* For NN, there is an `nn.Module` which wraps around the boring boiler-plate.
* A simple NN implementation is below for solving the MNIST dataset, instead of the CIFAR-10 dataset that the tutorial solves:

{% codeblock lang:py %}
import torch.nn.functional as F

class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.conv1 = nn.Conv2d(1, 1, 5)
        self.conv2 = nn.Conv2d(1, 1, 5)
        self.pool = nn.MaxPool2d(2, 2)
        self.fc1 = nn.Linear(1 * 10 * 10, 100)
        self.fc2 = nn.Linear(100, 10)

    def forward(self, x):
        x = F.relu((self.conv1(x)))
        x = F.relu(F.max_pool2d((self.conv2(x)), 2))
        x = x.view(-1, 1 * 10 * 10)
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        return F.log_softmax(x)
{% endcodeblock %}

As seen, in the `__init__` method, we just need to define the various NN layers we are going to be using. Then the `forward` method just runs through them. The `view` method is analogous to the NumPy `reshape` method.

The gradients will be applied after the backward pass, which is auto-computed. The code is self-explanatory and fairly easy to understand.

* Torch also keeps track of how to retrieve standard data-sets such as CIFAR-10, MNIST, etc.
* After getting the data, from the data-loader you can proceed to play with it. Below is an easy to understand implementation to complete the implementation (which is pretty much from the tutorial).

{% codeblock lang:py %}
# Create the net and define the optimization criterion
net = Net()
# The loss function
criterion = nn.CrossEntropyLoss()
# Which optimization technique will you apply?
optimizer = optim.SGD(net.parameters(), lr=0.001, momentum=0.5)

# zero the parameter gradients
optimizer.zero_grad()

for epoch in range(20):  # loop over the dataset multiple times
    # Run per epoch
    running_loss = 0.0
    for i, data in enumerate(trainloader, 0):
        # get the inputs
        inputs, labels = data

        # wrap them in Variable
        inputs, labels = Variable(inputs), Variable(labels)

        # zero the parameter gradients
        optimizer.zero_grad()

        # Forward Pass
        outputs = net(inputs)
        # Compute loss function
        loss = criterion(outputs, labels)
        # Backward pass and gradient update
        loss.backward()
        optimizer.step()
{% endcodeblock %}

* Assuming you are working on the tutorial. Try to solve the tutorial for MNIST data instead of CIFAR-10.
* Instead of the 3-channel (RGB) image of size 24x24 pixels, the MNIST images are single channel 28x28 pixel images.

Overall, I could get to 96% accuracy, with the current setup. The <a href="https://gist.github.com/reddragon/3fa9c3ee4d10a7be242183d2e98cfc5d">complete gist is here</a>.
