---
layout: page
title: Probability Theory
subtitle: Brushing up on the basics
---
<!-- following works -->
<!-- <script type="text/x-mathjax-config">
        MathJax.Hub.Config({
          TeX: { equationNumbers: { autoNumber: "AMS" } }
        });
        </script> -->

<div class="clearfix myquote" style="text-align:justify">
<img class="rightimg" src="/img/posts/prob_book_2.jpg" style="    max-height: 120px; width: auto">
I'm currently working my way through a few texts, one of which is the <i>fantastic</i> textbook:
<a href="https://www.amazon.com/Machine-Learning-Probabilistic-Perspective-Computation/dp/0262018020">Machine Learning: A Probabilistic Perspective</a>.  As the name of the textbook suggests, a solid understanding of probability theory is key.  As such, I'm revisiting some of my undergraduate notes.
</div>



## Probability Space
Note that some of the following definitions are taken directly from notes by <a href="https://www.stat.washington.edu/~nehemyl/">Néhémy Lim's</a>.

Consider the probability space $\left(\Omega, \mathcal{A}, \mathbf{P} \right)$, such that:

Let $\left(\Omega, \mathcal{A} \right)$ be a measurable space of events where:

* $\Omega$ is the sample space containing the set of all possible outcomes for a random experiment.
* $\mathcal{A}$ is the set of all subsets of $\Omega$ (including $\Omega$)--i.e. $\mathcal{A}\subseteq 2^{\Omega}$ (the power set).
<!-- **  $\mathcal{A}$ is given by $2^{\lvert\Omega\rvert}$ -->

#### Kolmogorov's axioms
Then a **probability measure** is a real-valued function such that: $\mathbf{P}:\mathcal{A}\to \mathbb{R}$ satisfying the following conditions:

1) **Non-Negativity** $\; \mathbf{P}(A) \ge 0 \; \forall A\in\mathcal{A}$

2) **Normalized** $\;\mathbf{P}\left(\Omega\right)=1$

3) **Additivity** $\; \mathbf{P}(A\cup B) = \mathbf{P}(A)+\mathbf{P}(B)$


The third condition can be generalized for any number of disjointed $A_i\in\mathcal{A}$ as:

\begin{equation}
\mathbf{P}\left( \bigcup_{i} A_i \right) = \sum_{i} \mathbf{P}(A_i)
\end{equation}




#### Conditional Probability
We begin with defining some properties.

The **conditional probability** given $B\in\mathcal{A}$ for any $A\in\mathcal{A}$ is:

\begin{equation}
\mathbf{P}\left(A\mid B\right)=
\frac{\mathbf{P}\left(A\cap B\right)}{\mathbf{P}(B)}
\end{equation}


#### multiplication rule
The numerator, $\mathbf{P}\left(A\cap B\right)$, is the probability of both $A$ and $B$ occurring and can be expressed in the following form, known as the **multiplication rule**:

\begin{equation}
\mathbf{P}(A\cap B)=\mathbf{P}(A\mid B)\cdot\mathbf{P}(B)
\label{eq:multi}
\end{equation}


More generally, for any number of $A_i \in \mathcal{A}$:

\begin{equation}
\mathbf{P}\left( \bigcap_{i} A_i \right) = \prod_{i} \mathbf{P}(A_i)
\end{equation}

Note that if $A$ and $B$ are disjointed sets (i.e. $A$ and $B$ are independent), then $\mathbf{P}(A\mid B)=\mathbf{P}(A)$ and Equation \eqref{eq:multi} becomes:

\begin{equation}
\mathbf{P}(A\cap B)=\mathbf{P}(A)\cdot\mathbf{P}(B)
\end{equation}


#### Probability of a union
Additionally, $\mathbf{P}\left(A\cup B\right)$, is the probability of either $A$ *or* $B$ occuring and can be expressed as:

$$
\begin{equation}
\mathbf{P}\left(A \cup B \right) =
\mathbf{P}(A) + \mathbf{P}(B) - \mathbf{P}(A \cap B)
\end{equation}
$$

And with the addition of a third event $C\in\mathcal{A}$:

$$
\begin{align}
\mathbf{P}\left(A \cup B\cup C \right) =
\; & \mathbf{P}(A) + \mathbf{P}(B) + \mathbf{P}(C)  \\
- \;&\mathbf{P}(A \cap B)- \mathbf{P}(A \cap C)- \mathbf{P}(B \cap C) \notag \\
+ \; &\mathbf{P}(A \cap B\cap C) \notag
\end{align}
$$

For the more general form involving $n$ events, we'll have to invoke the **inclusion–exclusion** to get the following closed form solution:

$$
\begin{equation}
\mathbf{P}\left(\bigcup_{i=1}^{n}A_{i}\right)=
\sum _{k=1}^{n}\left[(-1)^{k-1}\sum _{I\subseteq \{1,\ldots ,n\} \atop |I|=k}\mathbf{P} (A_{I})\right]
\end{equation}
$$

Where the last sum runs over all subsets $I$ of the indices $1, ..., n$ which contain exactly $k$ elements, and

$$
\begin{equation}
A_I \stackrel{\mathrm{def}}{=} \bigcap_{i\in I} A_i
\end{equation}
$$

Though for the most part, the $n\le3$ is most commonly used at this level of probability theory.



#### Bayes' Theorem
