---
layout: post
title: "Paper: Wide &amp; Deep Learning for Recommender Systems"
date: 2017-03-11 21:27:32 -0800
comments: true
categories:
---
There seems to be an interesting <a href="https://arxiv.org/abs/1606.07792" target="_blank">new model architecture for ranking & recommendation, developed by Google Research</a>. It uses Logistic Regression & Deep Learning in a single model.

This is **different from ensemble models**, where a sub-model is trained separately, and it's score is used as a feature for the parent model. In this paper, the authors learn a wide model (Logistic Regression, which is trying to "memorize"), and a deep model (Deep Neural Network, which is trying to "generalize"), **jointly**.

The input to the wide network are standard features, while the deep network uses <a href="https://en.wikipedia.org/wiki/Word_embedding" target="_blank">dense embeddings</a> of the document to be scored, as input.

The main benefits as per the authors, are:

1. DNNs can learn to over-generalize, while LR models are limited in how much they can memorize from the training data.

2. Learning the models jointly means that the 'wide' and 'deep' part are aware of each other, and the 'wide' part only needs to augment the 'deep' part.

3. Also, training jointly helps reduce the side of the individual models.

They also have a <a href="https://www.tensorflow.org/tutorials/wide_and_deep" target="_blank">TensorFlow implementation</a>. Also a <a href="https://www.youtube.com/watch?v=NV1tkZ9Lq48" target="_blank">talk on this topic</a>.

The authors employed this model to recommend apps to be downloaded to the user in Google Play, where they drove up app installs by 3.9% using the Wide & Deep model.

However, the Deep model in itself, drove up installs by 2.9%. It is natural to expect that the 'wide' part of the model should help in further improving the metric to be optimized, but it is unclear to me, if the delta could have been achieved by further bulking up the 'deep' part (i.e., adding more layers / training bigger dimensional embeddings, which are inputs to the DNNs).
