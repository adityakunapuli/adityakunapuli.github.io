---
layout: post
title: Probability Theory
subtitle: Brushing up on the basics
---
<!-- <p class="clearfix myquote" style="text-align:justify"> -->
<!-- <img class="rightimg" src="/img/posts/prob_book_2.jpg" style="    max-height: 120px; width: auto"> -->
I'm currently working my way through a few texts, one of which is the <i>fantastic</i> textbook:
<a href="https://www.amazon.com/Machine-Learning-Probabilistic-Perspective-Computation/dp/0262018020">Machine Learning: A Probabilistic Perspective</a>.  As the name of the textbook suggests, a solid understanding of probability theory is key.  As such, I'm revisiting some of my undergraduate notes.
<!-- </p> -->
$\newcommand{\P}[1]{\mathbf{P}\left(#1\,\right)}$


## Probability Space
Note that some of the following definitions are taken directly from notes by <a href="https://www.stat.washington.edu/~nehemyl/">Néhémy Lim's</a>.

Consider the probability space $\left(\Omega, \mathcal{A}, \mathbf{P} \right)$, such that:

Let $\left(\Omega, \mathcal{A} \right)$ be a measurable space of events where:

* $\Omega$ is the sample space containing the set of all possible outcomes for a random experiment.
* $\mathcal{A}$ is the set of all subsets of $\Omega$ (including $\Omega$)--i.e. $\mathcal{A}\subseteq 2^{\Omega}$ (the power set).
<!-- **  $\mathcal{A}$ is given by $2^{\lvert\Omega\rvert}$ -->

#### Kolmogorov's axioms
Then a **probability measure** is a real-valued function such that: $\mathbf{P}:\mathcal{A}\to \mathbb{R}$ satisfying the following conditions:

1) **Non-Negativity** $\; \P(A) \ge 0 \; \forall A\in\mathcal{A}$

2) **Normalized** $\;\P{\Omega}=1$

3) **Additivity** $\; \P{A\cup B} = \P{A}+\P{B}$


The third condition can be generalized for any number of disjointed $A_i\in\mathcal{A}$ as:

\begin{equation}
\mathbf{P}\left( \bigcup_{i} A_i \right) = \sum_{i} \P{A_i}
\end{equation}




#### Conditional Probability
The **conditional probability** given $B\in\mathcal{A}$ for any $A\in\mathcal{A}$ is:

\begin{equation}
\mathbf{P}\left(A\mid B\right)=
\frac{\mathbf{P}\left(A\cap B\right)}{\P{B}}
\end{equation}


#### Product Rule
The numerator, $\mathbf{P}\left(A\cap B\right)$, is the probability of both $A$ and $B$ occurring and can be expressed in the following form, known as the **product rule**:

<div class="outputTexSize">
$$
\begin{equation}
\P{A\cap B}=\P{A,B}=\P{A\mid B}\cdot\P{B}
\label{eq:multi}
\end{equation}
$$
</div>


More generally, for any number of $A_i \in \mathcal{A}$:

\begin{equation}
\mathbf{P}\left( \bigcap_{i} A_i \right) = \prod_{i} \P{A_i}
\end{equation}

Note that if $A$ and $B$ are disjointed sets (i.e. $A$ and $B$ are independent), then $\P{A\mid B}=\P{A}$ and Equation \eqref{eq:multi} becomes:

\begin{equation}
\P{A\cap B}=\P{A}\cdot\P{B}
\end{equation}


#### Summation Rule
Additionally, $\mathbf{P}\left(A\cup B\right)$, is the probability of either $A$ *or* $B$ occuring and can be expressed as:

<div class="outputTexSize">
$$
\begin{equation}
\mathbf{P}\left(A \cup B \right) =
\P{A} + \P{B} - \P{A \cap B}
\end{equation}
$$
</div>

And with the addition of a third event $C\in\mathcal{A}$:

<div class="outputTexSize">
$$
\begin{align}
\mathbf{P}\left(A \cup B\cup C \right) =
\; & \P{A} + \P{B} + \P{C}  \\
- \;&\P{A \cap B}- \P{A \cap C}- \P{B \cap C} \notag \\
+ \; &\P{A \cap B\cap C} \notag
\end{align}
$$
</div>

For the more general form involving $n$ events, we'll have to invoke the **inclusion–exclusion** to get the following closed form solution:

<div class="outputTexSize">
$$
\begin{equation}
\mathbf{P}\left(\bigcup_{i=1}^{n}A_{i}\right)=
\sum _{k=1}^{n}\left[(-1)^{k-1}\sum _{I\subseteq \{1,\ldots ,n\} \atop |I|=k}\mathbf{P} (A_{I})\right]
\end{equation}
$$
</div>


Where the last sum runs over all subsets $I$ of the indices $1, ..., n$ which contain exactly $k$ elements, and

<div class="outputTexSize">
$$
\begin{equation}
A_I \stackrel{\mathrm{def}}{=} \bigcap_{i\in I} A_i
\end{equation}
$$
</div>

Though for the most part, the $n\le3$ is most commonly used at this level of probability theory.



#### Bayes' Theorem

<div class="outputTexSize">
\begin{equation}
\P{A\mid\,B} = \frac{\P{B\mid\,A}\P{A}}{\P{B}}
\end{equation}
</div>


## Interlude: Combinatorics

#### Permutations
Disregarding the actual mathematical definition of a permutation, we instead look to the colloquial term for a permutation, also known as a **partial permutation**, the definition of which is $k$-permutations of $n$ are the different ordered arrangements of a $k$-element subset of an $n$-set.  The number of such $k$-permutations of $n$ (without repitition) is given by:

\begin{equation}
P(n,k) = \frac{n!}{(n-k)!}
\label{eq:perm}
\end{equation}


#### Combinations
If we have $n$ objects and we want to choose $k$ of them, we can find the total number of combinations by using the **Binomial Coefficient** (also known as $n$ choose $k$ or $nCk$):
\begin{equation}
\binom{n}{k} = \frac{n!}{(n-k)!k!}
\label{eq:binom}
\end{equation}

The total number of all possible combinations for all $k$-sized subsets of $n$ such that $0\le k \le n$:
\begin{equation}
{\sum _{k=0}^{n}{\binom {n}{k}}=2^{n}}
\end{equation}


Using Equation \eqref{eq:binom}, we can state the following:
* There are ${\tbinom {n}{k}}$ ways to choose $k$ elements from a set of $n$ elements.

<ul>
<!-- <pre> -->
    <li style="padding: 10px 0px;"><b>With Repetitions:</b> ${\tbinom {n+k-1}{k}}$</li>
    <li style="padding: 10px 0px;"><b>Binary:</b> There are ${\tbinom {n+k}{k}}$ strings containing $k$ ones and $n$ zeros</li>
    <li style="padding: 10px 0px;"><b>Binary:</b> There are ${\tbinom {n+1}{k}}$ strings consisting of $k$ ones and $n$ zeros such that no two ones are adjacent</li>
<!-- </pre> -->
</ul>
