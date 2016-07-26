---
layout: post
title: "Highlights of SIGIR 2016"
date: 2016-07-26 15:55:34 +0530
comments: true
categories:
---
This note contains highlights of SIGIR 2016 held at Pisa, Italy. SIGIR (Special Interest Group for Information Retrieval) is an annual conference related to new advances in Information Retrieval. I haven’t gone through all the papers yet, but sharing some highlights of the parts that I could attend / go through offline via the slides / proceedings.

{% img center /images/2016/07/pisa.png Tourists posing near the Leaning Tower. %}

## Day 1

The first day was dedicated to tutorials. Most tutorials were ‘survey’ like in the content, in that they did not present anything new, but were good if you want to get an idea about what’s happening in a particular area of IR.

**Deep Learning Tutorial**

This tutorial was conducted by members of the Huawei Labs, China. It was about the current state of Deep Learning in the industry.

* Went over basics like Convolutional Networks, Long Short Term Memory (LSTM), Embeddings, Recurrent Neural Networks, etc.
* Application of these techniques to Classification, Matching, Translation, Q&A answering, etc.
* <a href="http://www.hangli-hl.com/uploads/3/4/4/6/34465961/deep_learning_for_information_retrieval.pdf" target="_blank">Slides here</a>

**Succinct Data Structures**

This tutorial was about data-structures related to inverted indices. It went over both, theory (minimal and easy to understand), as well as a hands-on session. I really enjoyed this tutorial.

* Related to minimizing the space occupied by an inverted index, specifically about optimizing storage and lookups in posting lists. <a href="http://pages.di.unipi.it/rossano/succinct-data-structures-in-information-retrieval-theory-and-practice/" target="_blank">Link to the tutorial</a>
* Talked about <a href="http://www.di.unipi.it/~ottavian/files/partitioned_elias_fano_sigir14.pptx" target="_blank">Elias-Fano & Partitioned-Elias Fano encoding</a>.
* Practical task of constructing an inverted index for suggesting top-k keywords for a typeahead (based on wikipedia page titles).
* Demo-ed the use of their <a href="https://github.com/simongog/sdsl-lite" taget="_blank">Succinct Data Structures Library (SDSL)</a>.
* Described different data structures such as Wavelet trees, Suffix Arrays, Tries, etc.


## Day 2 & Day 3

The second day started with a keynote from Christopher Manning. Some highlights from the talk:

* His talk was about Natural Language Inference, and how Deep Learning can help with that.
* The primary goal was to be able to answer 4th grade science examinations.
* He talked about employing semantic embeddings between sentences and phrases for this.
* More detail about his talk <a href="http://nlp.stanford.edu/~manning/talks/SIGIR2016-Deep-Learning-NLI.pdf" target="_blank">here</a>.

Listing notes from few talks which were interesting:

**Learning to Rank with Selection Bias in Personal Search  (Google)**

* Personal Search is hard because human judgement is not possible on personal corpora such as GMail, GDrive.
* Personal Search is much sparser than web-search, as in for each searcher, the corpus almost entirely different. Hence we cannot use models which use a large number of click data for each query-document pair.
* Went over the explanation of Selection Bias: How queries with equal probabilities of appearing in the universe of all queries, can have different probabilities of appearing in the training set, because of selection bias.
* Introduced the inverse propensity bias, which is the ratio between the probability of the given query appearing in a random sample to the probability of the query appearing in the training set, and use that as a multiplicative weight for the loss function.
* They try to learn these weights in a global as well as segmented fashion. Where segmentation happens on query categories.
* They show improvements in online metrics as a result of accounting for selection biases.

**Fast and Compact Hamming Distance Index**

* This was another interesting talk, if you are interested in data-structures and efficiency work. The problem was to find all keys (assume fixed-size integers) in a given set $S$, which are at most distance $k$ away from a given key $Q$. Distance here is defined as the number of bits which differ.
* Applications are similarity detection / finding near duplications, image similarity. They use simhash to compute a hash of the document under question. Simhash has a property which is atypical of hash functions, in that it generates similar hashes for similar documents.
* They discussed several approaches like breaking each key into blocks of size $k$, and checking if at least one block matches with $Q$ (each key which passes this test is a candidate).
* Presented a Triangle Inequality approach, where $H(Q, P)$ $\leq$ $H(Q, K) + H(K, P)$. Where $H(A, B)$ is the hamming distance between $A$ & $B$. This is helpful in clustering together similar keys, and avoiding wasteful comparisons.

**Scalable Semantic Matching of Queries to Ads in Sponsored Search Advertising**

* The problem here was to match search queries to relevant ads.
* Used semantic embeddings to match queries to ads.
* All relevant ads had to have a minimum cosine similarity score, which was decided using offline ratings. Use skipped over ads as a negative signal.
* For training over large data-sets, they parallelize the training not by sharding the data, but by splitting the learning of contiguous non-overlapping range of the dense vector representations. That is, one trainer machine can learn [d0,...,d15], the other can learn [d16,..d31], and so on, but on the entire training data, using different random seeds.
* These partial embeddings are then stitched together.

## Day 4

Day 4 had talks from the Industry which talked about IR systems at scale (big / small). I found these to be very interesting. It’s sad that they were not recorded.

**Search Is Not a Box - Harad Shemtov (Google)**

* This talk went over Google Voice Search.
* About 50% of all searches come from Mobile. I found this number to be smaller than expected, given that Android + iOS usually account for significantly more than 50% in several metrics for other big products.
* 20% queries now come from voice. This number is huge, given voice is still relatively new.
* The speaker then went over the differences between Voice & Typed queries:
 Intent mix is different for voice v/s typed. The former has more of informational queries, like weather, movie times, game scores, etc.
* The results for these queries are built via curated knowledge graphs, featured snippets, etc.
* The searchers don’t look at multiple results for voice. This could be because they use voice in a hands-free mode, like when driving / cooking, etc.
* Voice has to support a conversational mode. Voice Search cannot be stateless, as there would be follow-up questions.
* Modules for Voice Search cannot optimize for clicks anymore.
* They support the ability to zoom into excerpts from matching documents, to be able to zoom into the precise answer. This was really cool.
* They went one level deeper with Google Now to proactively present results for queries you are likely to perform.

There was a related paper presented by Ido Guy from Yahoo! Research.

**Searching by Talking: Analysis of Voice Queries on Mobile Web Search**

* This paper has  a more deeper analysis of voice v/s web queries, along with backing data. I really recommend reading this paper, as it is very well written and received one of the several Best Papers award.
* More Q&A + audio/video sort of queries.
* Found that voice queries tend to be longer.
* Language used in voice search is very different:
    - Richer language such as "i'm looking for", "what is the", and even "please".
    - Higher Use of words which are harder to spell, but easy to say, such as "Mississippi", and avoidance of terms which are easier to spell, but harder to say, such as "2015".

**When Watson Went to Work - Aya Soffer (IBM Research)**

* IBM Research built Watson, and trained it to play Jeopardy as a way to demonstrate success in Q&A.
* They then exposed parts of Watson as cloud APIs (retrieval & ranking, sentiment analysis, entity tagging, etc.)
* Multiple applications within IBM for these modular APIs.
* She then talked in detail about how they are being used in Customer Care to build intelligent bots.

**Ask Your TV: Real-Time Question Answering with Recurrent Neural Networks - (Ferhan Ture, Comcast)**

* Comcast has built a ‘Voice Remote’, which should basically free the user from actually knowing the channel numbers / looking up the on-screen guide. It can take commands such as “HBO” (which will switch the channel to HBO).
* They also want it to support Q&As. Such as, "Tom Hanks Birthday", "Who played Donovan in Bridge of Spies?".
* Created synthetic Q&As using Knowledge Graphs. Like if they know attributes like { “person”: “Tom Hanks”, “birthday”: “01/01/1950”, “place-of-birth”: “USA” }, they can create questions like “Where was Tom Hanks born?”, “When was Tom Hanks born?”, etc.
* They then use RNNs for tagging entities, and classifying the question into a certain question type.
* They also added diversity into the way a question was phrased, using synonyms, to get a well-trained model independent of the way the searcher articulates. Also added noise into the training data.
* Used the keras toolkit which uses theano underneath, to write a quick script to train a model (apparently 5 lines to get boot-strapped).

**Amazon Search: The Joy of Ranking Products (Daria Sorokina)**

* Amazon has about 100 ML models for ranking products. They have one model per category (Electronics, Books, etc.) per site (US, Japan, India, etc.).
* They use GBDT as the training algorithm, with about 200 trees / model, and ~ 150 features per model.
* They use data from searcher behavior to train the models.
Positive Labels are like: Item was Clicked, Added to Cart, Purchased, Consumed (Applicable for Video / Music).
* Negative Labels are like: Ignored, Clicks on a random result placed in the top few results (indicates positional bias).
* Their result blending across different categories / verticals works as follows:
    - They use the Vertical Score as a feature
    - Relevance of the query for the given category / vertical.
    - Hunger Score: To introduce diversity in the results, each vertical has a score which is proportional to how long its results have not been included in the blended results.
* They use Probabilistic Context Free Grammars (PCFG) for query understanding. For example, “dress” in “dress shoes” is a modifier, but not in “casual dress”.
* They use reformulations as a signal to find related products.
* They semi-curate / bias results for certain queries, such as “diamond jewelry”.
    - In this case, if they optimize for CTR, products such as fake/cheap diamond jewelry would always get placed at the top.
    - They find certain queries for which they want to
    - They categorize their users into “fashionable” users, and use their training data to rank results for such queries.

**Learning to Rank Personalized Search Results in Professional Networks (Viet Ha-Thuc)**
* LinkedIn Search has different use-cases (recruiting, connecting, job seeking, sales, research, etc.)
* They would want to personalize the results for recruiters, job seekers, etc.
* Use LinkedIn “skills” as a way to cluster users, underlying assumption being that people with similar skills are likely to connect (while also removing unhelpful skills).
* Getting Intent Estimations for different intents.
* Use intent estimations for their federated search (people result, job result, group result, etc.)
* <a href="http://www.slideshare.net/VietHaThuc/learning-to-rank-personalized-search-results-in-professional-networks" target="_blank">Slides here</a>


## Day 5

The last day had workshops. I attended the first few talks of the NeuIR (Neural Network IR) workshop, before I had to leave to catch my flight.
The keynote was given by Tomas Mikolov from FAIR. His <a href="http://www.slideshare.net/BhaskarMitra3/recurrent-networks-and-beyond-by-tomas-mikolov
" target="_blank">slides are here</a>.

Key points:

* Gave a brief history of Recurrent Neural Networks (RNN), and their resurgence after 2010, when a key problem with the gradient descent (“exploding” gradients) was fixed. Also went through their applications.
* Simple Recurrent Networks (SRN) and Structurally Constrained Recurrent Nets (SCRN) as a way to store Longer Short Term Memory.
* SCRNs perform better than traditional LSTMs for large data. I couldn’t get much in terms of intuition as to why what he said was true.
* Rest of the talk comprised of discussing what an Intelligent Machine would comprise of.
* The idea is to train the machine (learner) on simple tasks, and it should be able to learn how to perform similar tasks without supervision, but through rewards.
The motivation is to be able to do well in general tasks, not just a specific application (like, say playing Go).
* The learner should be able to interact with humans and be able to search the internet and learn how to perform certain tasks. These are very ambitious goals.
Presented Stack RNNs, which can be used for tasks such as recognition of patterns like a^n b^n, or learning how to perform binary addition.


## Miscellaneous Papers I Glanced Over

**Statistical Significance, Power, and Sample Sizes: A Systematic Review of SIGIR and TOIS, 2006-2015**

* A thorough analysis of papers in the last 10 years, and a report regarding whether or not they used significance tests, which tests were used, and whether or not p-values and/or test statistics were reported.
* While number of papers where significance tests were being used has increased, the proportion of papers which report p-values and/or test statistics hasn't.
The authors also mention 'overpowered' cases, where the test/control populations were so large, a very tiny movement was also stat-sig (0.007% in the case of <a href="http://dl.acm.org/citation.cfm?id=2609617" target="_blank">this case</a>)

**Query to Knowledge: Unsupervised Entity Extraction from Shopping Queries using Adaptor Grammars**

* They try to extract out entities (product and brand) from shopping queries in an unsupervised fashion.
* They employ several steps to clean up the data (removing stop-words, re-ordering words to match known distributions of word groupings, i.e., replacing “head bobble” with “booble head”, for example).
* They use Probabilistic Context Free Grammars, which have several derivation trees for each rule, with associated probability to work on this cleaned up data.

**Explicit In Situ User Feedback for Search Results**

* Microsoft had <a href="http://i.imgur.com/QOvaQD5.jpg" target="_blank">an interesting poster</a>, where they demo-ed that they now ask for feedback regarding a certain result, after the searcher clicks on that result, but clicks on the back button.
* They then use these results along with offline raters, and try to correlate their offline relevance v/s user reports. Though there is inherent selection bias in this set, since searchers are likely to click on the back button mostly for unsatisfactory results and/or browsy behaviors.


## Overall

This was my first IR conference, and an academic conference in a long time. These are the key takeaways:

* Deep Learning has several applications in IR. This is true both for Industry as well as Academia.
    - Industrial talks were straight-forward applications around semantic understanding, query understanding, Q&A answering, etc.
    - Fun tidbit: It seems constructing very deep networks is in vogue, and a good way to get a paper accepted. One particular architecture presented during the conference had a convolutional layer, an LSTM layer, max-pooling, and a fully connected layer. When asked by the audience, if they tried a less deep network (because their problem didn’t seem complex enough), they responded that trying to go less deep was Future Work :-)
* I enjoyed the more ‘applied’ aspects of the conference, such as the tutorials, workshops, industrial talks and poster presentations.
* A significant fraction of the academic papers that I could go through, had very specific scope, not always well-thought in terms of scale, and sometimes not thorough in terms of stat-signess.
* I felt presentations could have been more effective with examples. I liked how some of efficiency papers, posters and industrial track talks were more driven by examples. People needing deeply technical details, can always refer to the papers.
* Enjoyed interacting with people from different places (such as Microsoft, Academia, small startups (scale small enough that they can take short-cuts)), and understand their perspective.
