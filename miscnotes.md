---
layout: page
title: Miscellaneous Math Notes
subtitle: Just a collection of random math notes
---

# Neural Networks
<div style="text-align:center; width=768px;">
  <a href="http://cs231n.github.io/linear-classify/">
    <input  type="button"
            class="bigButton"
            value="Stanford CS231n Notes"
            href="http://cs231n.github.io/linear-classify/"/>
  </a>
</div>

**Gradient Descent**

 $$
 \begin{equation}
\nabla ={\frac {\partial}{\partial x}}\mathbf {i} +{\frac {\partial}{\partial y}}\mathbf {j} +{\frac {\partial}{\partial z}}\mathbf {k}
\end{equation}
 $$

## Activation Functions
**Logistic Function**

$$
\begin{equation}
P(x)= \frac{1}{1+e^{-k(x-x_0)}}
\end{equation}
$$

**SoftMax**

$$
P(y=j\mid \mathbf {x} )={\frac {e^{\mathbf{x} ^{\mathsf{T}}\mathbf{w}_{j}}}{\sum_{k=1}^{K}e^{\mathbf {x} ^{\mathsf {T}}\mathbf{w}_{k}}}}
$$




## Cross Entropy Loss
Cross-entropy loss, or log loss, measures the performance of a classification model whose output is a probability value between 0 and 1. Cross-entropy loss increases as the predicted probability diverges from the actual label. So predicting a probability of .012 when the actual observation label is 1 would be bad and result in a high loss value. A perfect model would have a log loss of 0.

 $$
 \begin{equation}
\mathcal{L}_o = -\sum_{c=1}^{M}{\delta(o,c)\log(p_{o,c})}
\end{equation}
 $$

Where:
* $ M $ - number of classes (dog, cat, fish)
* $ \log $ - the natural log
* $ y $ - binary indicator if class label $ c $ is the correct classification for observation $ o $
* $ p $ - predicted probability observation $ o $ is of class $ c $

## Multi-Label vs Multi-Class
If you have a multi-label classification problem = there is more than one "right answer" = the outputs are NOT mutually exclusive, then use a sigmoid function on each raw output independently. The sigmoid will allow you to have high probability for all of your classes, some of them, or none of them. Example: classifying diseases in a chest x-ray image. The image might contain pneumonia, emphysema, and/or cancer, or none of those findings.

If you have a multi-class classification problem = there is only one "right answer" = the outputs are mutually exclusive, then use a softmax function. The softmax will enforce that the sum of the probabilities of your output classes are equal to one, so in order to increase the probability of a particular class, your model must correspondingly decrease the probability of at least one of the other classes. Example: classifying images from the MNIST data set of handwritten digits. A single picture of a digit has only one true identity - the picture cannot be a 7 and an 8 at the same time
[Link](https://stats.stackexchange.com/a/410112)


# Decision Trees
**See following for better explanations:** [1](https://www.saedsayad.com/decision_tree.htm) [2](https://medium.com/deep-math-machine-learning-ai/chapter-4-decision-trees-algorithms-b93975f7a1f1) [3](https://github.com/rasbt/python-machine-learning-book/blob/master/faq/decision-tree-binary.md).

Our objective function (e.g., in CART) is to maximize the information gain (IG) at each split. In practice both Gini Impurity and Entropy typically yield very similar results and it is often not worth spending much time on evaluating trees using different impurity criteria rather than experimenting with different pruning cut-offs.

## Classification and Regression Trees (CART)
**Gini Impurity**

Given a set of items with $J$ classes, suppose $$i\in \{1,2,...,J\$$}, and let $$p_i$$ be the fraction of items labeled with class $$i$$ in the set.

$$
\begin{align}
	I_G(p) &= \sum _{i=1}^{J}p_{i}\sum _{k\neq i}p_{k} \\
	&=\sum _{i=1}^{J}p_{i}(1-p_{i}) \\
	&=\sum _{i=1}^{J}(p_{i}-{p_{i}}^{2}) \\
	&=\sum _{i=1}^{J}p_{i}-\sum _{i=1}^{J}{p_{i}}^{2} \\
	&=1-\sum _{i=1}^{J}{p_{i}}^{2}
\end{align}
$$

**Iterative Dichotomiser 3 (ID3)**

Steps:
1. Compute the entropy for data-set
2. For every attribute/feature:
    1. Calculate entropy for all categorical values
    2. Take average information entropy $H\left(S\|A\right)$ for the current attribute
    3. Calculate gain for the current attribute
3. Pick the highest gain attribute.
4. Repeat until we get the tree we desired.


### Information Gain $$IG(S,A)$$
Information gain $$IG(A)$$ is the measure of the difference in entropy from before to after the set $$S$$ is split on an attribute $$A$$. In other words, how much uncertainty in $$S$$ was reduced after splitting set $$S$$ on attribute $$A$$.

 $$
 \begin{equation}
IG(S,A)=H(S)-\sum_{t\in T}p(t)H(t)=H(S)-H(S|A)
\end{equation}
 $$


Where $H\left(S\|A\right)$ is the average information entropy for a given attribute.

### Entropy $H(S)$
Entropy is the measure of *(im)purity of an arbitrary collection of examples* and is given by:

$$
\begin{equation}
H(S) = \sum_{x\in X}{-p(x)\log_2{p(x)}}
\end{equation}
$$

Where:
1. $$S$$ is the current dataset
2. $$X$$ is the set of unique classes/labels/targets within $$S$$
3. $$p(x)$$ is the proportion of the number of elements in class $$x$$ to the number of elements in set $$S$$

# Statistics
## Normal Distribution

 $$
 \begin{equation}
\mathcal{N}(\mu,\sigma) = f(x\mid \mu ,\sigma ^{2})={\frac {1}{\sqrt {2\pi \sigma ^{2}}}}e^{-{\frac {(x-\mu )^{2}}{2\sigma ^{2}}}}
\end{equation}
 $$


Where $$\sigma$$ is the standard deviation, $$\sigma^2$$ is the variance and $$\mu$$ is the mean.
## Binomial Probability
The probability of getting exactly $k$ successes in $n$ trials is given by the probability mass function:
\begin{align}
\Pr(k;n,p) &={\binom {n}{k}}p^{k}(1-p)^{n-k} \\
&= \frac{n!}{k!(n-k)!}p^{k}(1-p)^{n-k}
\end{align}
The following is known as the binomial coefficient

 $$
 \begin{equation}
{\binom {n}{k}}=\frac{n!}{k!(n-k)!}
\end{equation}
 $$

The formula can be understood as follows. $$k$$ successes occur with probability $$p^k$$, and $$n-k$$ failures occur with probability $$(1-p)^{n-k}$$.


# K-Means Clustering
Reduces dimensions.
>**Curse of Dimensionality**: As the number of features or dimensions grows, the amount of data we need to generalize accurately grows exponentially
