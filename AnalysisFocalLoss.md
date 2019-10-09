---
layout: page
title: RetinaNet Analysis
subtitle: Focal Loss for Dense Object Detection
---


<p class="myquote">
	This paper analyzes the novel implementation of a weighting factor to the loss function as outlined in the article "Focal Loss for Dense Object Detection"  by Lin et al..  The author's coin the term "focal loss" for this weighting factor and its purpose is to modulate the effects of class imbalances in context of single-stage detectors. The analysis portion concludes by demonstrating that the performance of focal loss exceeded not only the current leading single-stage detection algorithms, but also leading two-stage algorithms as well.  The final section contains example images of the author's own implementation.
</p>

# Problem Statement
The primary motivation behind the introduction of focal loss is to improve performance of one-stage detectors, specifically in context of dealing with large class imbalances, a problem that two-stage detectors don't posses.  The specifics of the two families of detection algorithm is explored in detail below.


## Two Stage Detection
The problem of *object detection* fundamentally differs from *object classification* in that the purpose of the former is to detect the areas within an image that have a high probability of containing objects of interest.

The current state-of-the-art frameworks for object detection utilize a two stage process in which:
1. the first stage, utilizing a Region Proposal Network (RPN), generate sparse set of *region proposals* that cover Regions of Interest (ROI), and
2. the second stage, which utilizes a Convolutional Neural Network (CNN) to classify each proposal as either one of the foreground classes or as background.

The family of two-stage methodologies, such as R-CNN , Fast R-CNN , Faster R-CNN , Mask R-CNN  or some variants of these four archetypes, continue to demonstrate the highest average precision in COCO (AP COCO) evaluations .

Though the most immediately apparent side-effect of two-stage models and their associated AP, is that they are also computationally demanding.  This can be attributed in large part to their requirement for very large input sizes, which in turns is a prerequisite for the ROI Pooling operations .  The end result is the first stage produces a large number of candidate boundary boxes for each image, that is then fed into a CNN for classification.



## Single Stage Detection
In comparison, a new family of object detectors that prioritizes speed over accuracy, has emerged and quickly gained popularity.  These models, called Single Shot Detectors (SSD), combine the process of boundary box prediction and classification into a single stage.

<figure>
	<figcaption class="figcap" >
		<b>Table 1</b>: Performance of various One-Stage Models.
	 </figcaption>
<table class="analysis-tg" style="width: 75%;">
   <tr>
      <th class="analysis-tg-header">Detector</th>
      <th class="analysis-tg-header">Backbone</th>
      <th class="analysis-tg-header">AP</th>
   </tr>
   <tr>
      <td class="analysis-tg-cell">YOLOv2</td>
      <td class="analysis-tg-cell">DarkNet-19</td>
      <td class="analysis-tg-cell">21.6</td>
   </tr>
   <tr>
      <td class="analysis-tg-cell">SSD513</td>
      <td class="analysis-tg-cell">ResNet-101-SSD</td>
      <td class="analysis-tg-cell">31.2</td>
   </tr>
   <tr>
      <td class="analysis-tg-cell">DSSD513</td>
      <td class="analysis-tg-cell">ResNet-101-DSSD</td>
      <td class="analysis-tg-cell">33.2</td>
   </tr>
</table>
</figure>



As described, these models prioritize speed over accuracy, as such with the resulting decrease in computation time and computational resources, comes reduced performance.  Table 1 shows a performance comparison between the various Single Shot Detection models. [^1] Though nonetheless, there are many cases in which such a trade off is worth it, such as when used in consumer mobile devices.

[^1]:For a much more thorough survey in performance differences between current architectures, see . Figure 10 at the end of this analysis shows one of the results of the survey.

A much more compelling problem arises in Single Stage Detectors--namely that of *class imbalance*.  Specifically, the *intrinsic imbalance* that arises in naturally occurring frequencies of data --*e.g.* medical diagnoses of cancer in a large population of healthy patients.  In context of object detection models, Lin et al. summarized the problem as thus:
> These detectors evaluate $10^4-10^5$ candidate locations per image but only a few locations contain objects.


The issue of class imbalances and their effects on back-propagation algorithms within shallow neural nets has been documented and studied since at least the early 1990s.  Anand et al. showed that the effect of class imbalances led to the majority class dominating the net gradient .  The figure below  demonstrates this--note that the error associated with the majority class quickly declines, whereas the error associated with the minority class essentially explodes until the model is *actually performing worse than simply flipping a coin*.  Or to put it another way: as a result of severe class imbalances, the model shown  is performing so poorly in respect to the minority class, that actual prediction may be improved by reversing the assignment of probabilities (in a binary classification).






<figure  class="centerimg" style="width:75%;" >
  	<figcaption class="figcap" >
	<b>Figure 1</b>: Effect of class imbalances.
	</figcaption>
  <img src="{{site.url}}/assets/focalloss/webp/Anand.webp" alt=""/>
</figure>


# Approach
## Focal Loss
We begin by introducing the definition of $$\text{Cross Entropy (CE)}$$ loss in the case of binary classification:

$$
\begin{equation}
\text{CE}\left(p,y\right) =
\begin{cases}
-\log\left(p\right) & \text{if } y=1 \\
-\log\left(1-p\right) & \text{otherwise}
\end{cases}
\end{equation}
$$

Where $$y\in\left\{\pm 1\right\}$$ describes the ground truth class and $$p\in\left[0,1\right]$$ is the model's estimated probability for a given class with label $$y=1$$.  Rewriting the $$p$$ equation such that

$$
\begin{equation}
p_t=
\begin{cases}
p & \text{if } y=1 \\
1-p & \text{otherwise}
\end{cases}
\end{equation}
$$

Allows us to rewrite $\text{CE}$ such that:

$$
\begin{equation}
\text{CE}(p,y) = -\log{(p_t)}
\end{equation}
$$


To reiterate: the problem at hand is dealing with large classes imbalances in single step detectors.  Such imbalance overwhelm the cross-entropy loss; easy to classify negatives (*i.e.* easy negatives) end up contributing the majority of the loss and dominate the gradient.  In terms of medical diagnoses, this would be the equivalent of attempting to create a model for predicting cancer by studying a population of primarily cancer-free patients.  In such scenarios, the easy negatives (i.e. cancer-free patients) would end up defining the model.  Whereas, in reality we are truly interested in the population with cancer.

A method common in dealing with this class imbalance problem is the introduction of a weighting factor $$\alpha$$ to the cross-entropy loss function such that:

$$
\begin{equation}
\alpha_t=
\begin{cases}
\alpha & \text{if} y=1 \\
1-\alpha & \text{otherwise}
\end{cases}
\end{equation}
$$

Where $$\alpha\in\left[0,1\right]$$.  This modification of $$\text{CE}$$ is known as *balanced cross entropy*.  The addition of this weighting factor helps to balance the respective importance of positive and negative training examples

Utilizing the aforementioned example of modeling cancer, the introduction of $$\alpha$$ would now allow us to increase contributions to the model from the minority class (*i.e.* patients with cancer), while simultaneously decreasing the role of the majority class.

And while this is a step in the right direction, $$\alpha$$ makes no additional distinction in the contributions from easy and hard examples.

To deal with this inability to distinguish easy and hard samples, the author's introduced  a new factor in place of $$\alpha$$ called *focal loss*, which they defined as:

$$
\begin{equation}
\text{FL}(p_t)=-(1-p_t)^\gamma\log{(p_t)}
\end{equation}
$$

The coefficient $$-(1-p_t)^\gamma$$ is known as the *modulating factor*, where $$\gamma$$ is a tunable *focusing hyperparameter*.  Figure 2 shows how choice of $$\gamma$$ can influence loss.  Note that the case of $$\gamma=0$$ (*i.e.* the top-most line in blue) corresponds to the normal cross entropy loss function.


<figure  class="centerimg" style="width:75%;" >
  <figcaption style="text-align:center;">
		Figure 2: Loss for varying values of $\gamma$.
	</figcaption>
  <img src="{{site.url}}/assets/focalloss/webp/CEloss.webp" alt=""/>
</figure>


Revisiting the following equation from above:

$$
\begin{equation}
p_t=
\begin{cases}
p & \text{if } y=1 \\
1-p & \text{otherwise}
\end{cases}
\end{equation}
$$

 in conjunction with Figure [2](#figure-2) we can observe that the focal loss function has the following properties:

 1. Misclassifications associated with a high probability assignment (*i.e.* if $$y\neq1$$ and the associated $$p$$ is large), result in the $$(1-p_t)\to1$$ and hence the loss term remains unchanged.
 2. Alternatively, in cases of correct classification with a high probability $$(y=1 \text{ and } p\to1)$$ or misclassifications with low probability both result in $$p_t\to1$$ and hence $$(1-p_t)\to0$$ and the loss contribution for that example is reduced.
 3. The focusing parameter $$\gamma$$ smoothly adjusts the rate at which easy example's loss contribution is reduced.

A summary of the various effects to the loss function is provided in Table 2.

<figure>
<figcaption class="figcap" >
   <b>Table 2</b>: Changes to loss.
</figcaption>
<table style="margin-left: auto;margin-right: auto; ">
   <tbody>
      <tr>
         <td></td>
         <td><b>High</b> $p$</td>
         <td><b>Low</b> $p$</td>
      </tr>
      <tr>
         <td><b>Correct</b></td>
         <td>Reduce Loss</td>
         <td>Loss Unchanged</td>
      </tr>
      <tr>
         <td><b>Incorrect</b></td>
         <td>Loss Unchanged</td>
         <td>Reduce Loss</td>
      </tr>
   </tbody>
</table>
</figure>


# Experimental Setup
The author's implemented the focal loss function into a Feature Pyramid Network (FPN) backbone, which itself rests upon the ResNet architecture .  As the backbone itself is, in the author's own words. an **"off the shelf convolutional network"**, we're not going to cover any additional detail to that end.  The model was trained with Stochastic Gradient Descent (SGD) against the [COCO trainval135k dataset](http://cocodataset.org/), utilizing 80k images for training and a random sample of 35k images for testing  pulled from the validation set.

# Analysis

Figure 3 shows the results of varying $$\gamma$$ on cumulative loss for positive and negative samples, once the model had converged.   The effects of changing $$\gamma$$ for the positive samples was minor, though for the negative samples, greater values of $$\gamma$$	 had the effect of focusing the accumulated loss on the the hard examples--*i.e.* severely reducing the contribution of easy negatives.  These finding match the predictions made in Table 2.

<figure  class="centerimg" style="width:75%;" >
  	<figcaption class="figcap" >
	<b>Figure 3</b>: Accuracy vs Time of various architectures.
	</figcaption>
  <img src="{{site.url}}/assets/focalloss/webp/results1.webp" alt=""/>
</figure>

The author's additionally note that the precise form function used for the modulating factor is not critical.  They demonstrate this by testing focal loss with the following modulating factor:

$$
\begin{align}
p_t^2&=\sigma(\gamma x_t+\beta) \\
\text{FL}^\star&=-\frac{1}{\gamma}\log{\left(p_t^\star\right)}
\end{align}
$$

The differences between $$\text{FL}$$ and $$\text{FL}^\star$$ are trivially minor as shown in Table 3:

<figure  class="centerimg" style="width:75%;" >
  	<figcaption class="figcap" >
	<b>Table 3</b>: Results of $\text{FL}$ and alternative, $\text{FL}^\star$.
	</figcaption>
<table style="margin-left:auto; margin-right:auto;">
<thead><tr><th>$\text{Loss}$</th><th>$\gamma$</th><th>$\beta$</th><th>$\text{AP}$</th></tr></thead><tbody>
<tr><td>$\text{CE}$</td><td>—</td><td>—</td><td>31.1</td></tr>
 <tr><td>$\text{FL}$</td><td>2</td><td>-</td><td>34.0</td></tr>
 <tr><td>$\text{FL}^\star$</td><td>2</td><td>1</td><td>33.8</td></tr>
 <tr><td>$\text{FL}^\star$</td><td>4</td><td>0</td><td>33.9</td></tr>
</tbody></table>
</figure>

# Results
### Work in progress, though example images (taken from my own library):

![](/assets/focalloss/webp/retinanetExample1.webp)


-----
