---
layout: page
title: Elementary Probability Theory
subtitle: Brushing up on the basics
---

<div class="clearfix" style="text-align:justify">
<img class="rightimg" src="/img/posts/prob_book_2.jpg">
Thanks to COVID-19, and all the free time I now have, I've decided to begin working my way through a textbook that we partially used in my statistical computing course:
<a href="https://www.amazon.com/Machine-Learning-Probabilistic-Perspective-Computation/dp/0262018020">Machine Learning: A Probabilistic Perspective</a>

Though in the course of working my way through the textbook, it became obvious that I had forgotten a good deal of the probability theory that I had originally picked up in my undergrad.  The following notes are to help me.
</div>




<br>
## Probability Space
Consider the probability space $\left(\Omega, \mathcal{A}, \mathbf{P} \right)$, such that:

Let $\left(\Omega, \mathcal{A} \right)$ be a measurable space of events where:

* $\Omega$ is the sample space containing the set of all possible outcomes.
* $\mathcal{A}$ is the set of all subsets of $\Omega$ (including $\Omega$)--i.e. $\mathcal{A}\subseteq 2^{\Omega}$ (the power set).
<!-- **  $\mathcal{A}$ is given by $2^{\lvert\Omega\rvert}$ -->

#### Kolmogorov's axioms
Then a **probability measure** is a real-valued function such that: $\mathbf{P}=\mathcal{A}\to \mathbb{R}$ satisfying the following conditions:

1) **Non-Negativity** $\; \mathbf{P}(A) \ge 0 \; \forall A\in\mathcal{A}$

2) **Normalized** $\;\mathbf{P}\left(\Omega\right)=1$

3) **Additivity** $\; \mathbf{P}(A\cup B) = \mathbf{P}(A)+\mathbf{P}(B)$


The third condition can be generalized for any number of disjointed $A_i\in\mathcal{A}$:

$$\mathbf{P}\left( \bigcup_{i} A_i \right) = \sum_{i} \mathbf{P}(A_i)$$




#### Conditional Probability
We begin with defining some properties.

The **conditional probability** given $B\in\mathcal{A}$ for any $A\in\mathcal{A}$ is:

$$
\mathbf{P}\left(A\mid B\right)=
\frac{\mathbf{P}\left(A\cap B\right)}{\mathbf{P}(B)}
$$

#### multiplication rule
The numerator, $\mathbf{P}\left(A\cap B\right)$, is the probability of both $A$ and $B$ occurring and can be expressed in the following form, known as the **multiplication rule**:

$$
\mathbf{P}(A\cap B)=\mathbf{P}(A\mid B)\cdot\mathbf{P}(B)
$$

More generally, for any number of $A_i \in \mathcal{A}$:

$$
\mathbf{P}\left( \bigcap_{i} A_i \right) = \prod_{i} \mathbf{P}(A_i)
$$

#### Probability of a union
Additionally, $\mathbf{P}\left(A\cup B\right)$, is the probability of either $A$ *or* $B$ occuring and can be expressed as:

$$
\mathbf{P}\left(A \cup B \right) =
\mathbf{P}(A) + \mathbf{P}(B) - \mathbf{P}(A \cap B)
$$

And with the addition of a third event $C\in\mathcal{A}$:

$$
\begin{align}
\mathbf{P}\left(A \cup B\cup C \right) =
\; & \mathbf{P}(A) + \mathbf{P}(B) + \mathbf{P}(C) \\
- \;&\mathbf{P}(A \cap B)- \mathbf{P}(A \cap C)- \mathbf{P}(B \cap C) \\
+ \; &\mathbf{P}(A \cap B\cap C)
\end{align}
$$

For the more general form involving $n$ events, we'll have to invoke the **inclusion–exclusion** to get the following closed form solution:

$$
\mathbf{P}\left(\bigcup_{i=1}^{n}A_{i}\right)=
\sum _{k=1}^{n}\left[(-1)^{k-1}\sum _{I\subseteq \{1,\ldots ,n\} \atop |I|=k}\mathbf{P} (A_{I})\right]
$$

Where the last sum runs over all subsets $I$ of the indices $1, ..., n$ which contain exactly $k$ elements, and

$$
A_I \stackrel{\mathrm{def}}{=} \bigcap_{i\in I} A_i
$$



Note that if $A$ and $B$ are disjointed sets (i.e. $A$ and $B$ are independent), then $\mathbf{P}(A\mid B)=\mathbf{P}(A)$.

#### Bayes' Theorem
