---
title: "Model Pruning"
date: 2018-10-22T11:23:28+08:00
tags: ["Model Pruning"]
categories: ["Literature Review"]
---

Deep learning has been prevailing for years in computer vision community.
It has become a de-factor standard in various sub-domains of computer vision,
e.g. face recognition, object detection, semantic segmentation, etc. However,
the heavy computation load accompanied with any deep learning model renders it
improbable, if not impossible, to be deployed on resource-constraint devices
such as mobile phones. Various methods are proposed to reduce memory footprint
and latency on these models. The majority of these methods can be categorized into 
the following classes:

* Develop more efficient network architecture. For example, by utilizing the power of residual
branch, ResNet exhibits better performance than AlexNet under even tighter
computation resource budget. However, the advent of efficient network
architecture relies on human expertise to a great extent. To make the process
more ''scalable'', network architecture search (NAS[^nasnet]) methods are proposed to
automatically find better network architectures, thus human effort is reduced
to the lowest level possible. We'll not cover NAS here today, as NAS is another
big topic that cannot be fully developed in a few words.
* Weight approximation. This is a broad category, in that any method that
attempts to tradeoff network preciseness against latency or memory footprint
can be considered as one practice of weight approximation. In other words, we
do not attempt to preserve the output value strictly in a binary sense --- after all 
deep learning is not that sort of science of absolute exactness. What we are 
pursuing is to sacrifice a little exactness, in exchange for smaller model and
faster speed. Quantization[^quantization] is one common practice of weight
approximation. Low-rank approximation, such as SVD, is another effective approach.
* Model pruning. Here comes the main topic today. Model pruning refers to the
practice of eliminate unimportant connections in the network, thus the model
size and model running time can be drastically reduced without much accuracy loss.

According to the pruning target, model pruning methods can be classfied into two
groups: fine-grained and coarse-grained. As the name suggests, fine-grained
pruning operates at a finer granularity. Normally, for fine-grained pruning, 
weight connections within one convolution layer can be controlled separately.
Deep Compression[^deep-compression] is a notable example of fine-grained
pruning. However, to make fine-grained pruning effective, it generally requires
specially designed hardware to make use of the sparsity. Commodity products 
such as x86 and ARM CPUs are unable to leverage the sparsity to gain any 
practical acceleration. In contrast, coarse-grained pruning removes part of the
convolution as a whole. Usually the pruned part is considered to be following
some sort of pattern, e.g. a whole channel being pruned out [^channel-pruning] [^amc],
utilizing group convolution [^group-approximation], or exhibiting block-level
sparsity [^block-sparse]. Since the pattern-based nature, coarse-grained pruning 
has another name, *structured pruning*, to emphasize that an inherent structure
resides in the pruning criteria. Coarse-grained pruning does not impose any requirement
on the deployed device, thus it has a broader applicability. We'll only cover
coarse-grained pruning in this blog post.

Conventional pruning pipeline consists of three stages: 
training, pruning, and fine-tuning [^rethinking]. Assuming that the pruning
happens at channel granularity, then two important decisions the pruning
agent has to make are 

1. How many channels will be removed at current layer;
2. Which set of channels should be removed. 

To answer the first question, reinforcement-learning-based approaches are
proposed [^amc], in which an RL agent is trained to give out the percentage of
the number of channels to be removed. NetAdapt [^netadapt] runs the model
on the targeting device with different pruning settings, and select the best
one according to the profiled running time. Coreset-based approach [^coreset] sets
the appropriate ratio within affordable accuracy loss. Some work does not even take
the problem into consideration, e.g. a predefined pruning ratio is used
[^channel-pruning].

For the second question, a uniformly agreed view is lacking. Channel pruning[^channel-pruning]
introduces a channel mask and solves the problem by LASSO regression. NetAdapt[^netadapt]
simply ranks the channel importance by its \\(l2\\)-norm and removes the least
important ones. NISP[^nisp] assigns importance score to neurons by its impact
on the final output, and removes neurons according to the importance score.
What's even more interesting is the viewpoint presented by Z. Liu et al. [^rethinking], which
totally invalidates the efficacy and the importance of channel selection, and argues
that the difference would be minor for any channel selection method. A randomly
selecting strategy would behave no different than an intricately-designed one,
as it is the pruned *network architecture* that matters, rather than the remaining
weight. Indeed this viewpoint shocks me, but I'm neither convinced nor totally
disagree about the idea.

Let's return to the pruning pipeline and take a look at the third stage,
finetuning. Finetuning is the mechanism to recover the network accuracy caused
by pruning, and it is generally accepted as an effective approach. However,
finetuning requires much computation power and it is sometimes undesirable.
Some works employ error reconstruction in place of or in addition to finetuning,
which exhibit similar performance under less computation resource 
budget [^channel-pruning] [^amc] [^thinet]. 
Error reconstruction refers to the weight adjusting operation after pruning, 
with the goal of minimizing the per-layer output error. For \\(l2\\)-loss,
it can be formulated as a linear regression problem and is directly solvable.
Even with error reconstruction, it is a typical practice to perform
long-term finetuning to fully recover the network accuracy at the end of the
whole pruning process.

As a frontier research topic, model pruning has aroused attention of
the deep learning community. It is an effective approach to reduce model size
and make it more desirable to deploy on resource-constraint platforms. We aim
to make the process as smooth as possible, without much human intervention.
Let's see if it works :)

[^coreset]: A. Dubey, M. Chatterjee, and N. Ahuja. Coreset-Based Neural Network Compression. https://arxiv.org/abs/1807.09810
[^group-approximation]: B. Peng, W. Tan, Z. Li, S. Zhang, D. Xie, and S. Pu. Extreme Network Compression via Filter Group Approximation. https://arxiv.org/abs/1807.11254
[^nasnet]: B. Zoph, V. Vasudevan, J. Shlens, and Q. V. Le. Learning Transferable Architectures for Scalable Image Recognition. https://arxiv.org/abs/1707.07012
[^thinet]: J. H. Luo, J. Wu, and W. Lin. ThiNet: A Filter Level Pruning Method for Deep Neural Network Compression. https://arxiv.org/abs/1707.06342
[^quantization]: R. Krishnamoorthi. Quantizing deep convolutional networks for efficient inference: A whitepaper. https://arxiv.org/abs/1806.08342
[^nisp]: R. Yu, A. Li, C. F. Chen, J. H. Lai, V. I. Morariu, X. Han, M. Gao, C. Y. Lin, and L. S. Davis. NISP: Pruning Networks using Neuron Importance Score Propagation. https://arxiv.org/abs/1711.05908
[^block-sparse]: S. Gray, A. Radford, and D. P. Kingma. GPU Kernels for Block-Sparse Weights. https://s3-us-west-2.amazonaws.com/openai-assets/blocksparse/blocksparsepaper.pdf
[^deep-compression]: S. Han, H. Mao, and W. J. Dally. Deep Compression: Compressing Deep Neural Networks with Pruning, Trained Quantization and Huffman Coding. https://arxiv.org/abs/1510.00149
[^netadapt]: T. J. Yang, A. Howard, B. Chen, X. Zhang, A. Go, M. Sandler, V. Sze, and H. Adam. NetAdapt: Platform-Aware Neural Network Adaptation for Mobile Applications. https://arxiv.org/abs/1804.03230
[^amc]: Y. He, J. Lin, Z. Liu, H. Wang, L. J. Li, and S. Han. AMC: AutoML for Model Compression and Acceleration on Mobile Devices. https://arxiv.org/abs/1802.03494
[^channel-pruning]: Y. He, X. Zhang, and J. Sun. Channel Pruning for Accelerating Very Deep Neural Networks. https://arxiv.org/abs/1707.06168
[^rethinking]: Z. Liu, M. Sun, T. Zhou, G. Huang, and T. Darrell. Rethinking the Value of Network Pruning. https://arxiv.org/abs/1810.05270
