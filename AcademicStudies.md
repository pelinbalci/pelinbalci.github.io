---
layout: page
title: Academic Studies
permalink: /Academic Studies/
---

## Lectures
- [Yarin Gal -. Bayesian Deep Learning](https://www.youtube.com/watch?v=G6tUZRHnJYc&t=941s)
- [Bayesian Deep Learning](https://www.cs.ox.ac.uk/people/yarin.gal/website/bdl101/)

**Bayesian Probability Theory - the Language of Ucertainty:**
- Would you pay a penny (0.01 pound) to buy a note where I commit to paying 1 pound instead?
- Would you pay a penny (0.99pound) to buy a note where I commit to paying 1 pound instead? 
- Would you sell a unit wager at p for heads? Yu get p and you have to pay 1 pound if head.

I think he expected outcome will be 0.5 heads. Which means 0.5*1*note It need to be less than p*1*note for buyer and higher than p*1*note for seller. 

p captures our degree of belief aout the event A (or head) taking place. (aka uncertainty, confidence).

Second Game: 
- note1:  outcome = head
- note2 : outcome = tails

You decide p for note 1 and q for note2, I decide whether to buy from you or sell you each note at the price you determine. 

- if p+q <1, I will buy the notes. I'm guarenteed to make money. Ex: you said note1 (head) 0.1, note2 (tail) 0.4. 
Based on my selection you will give me 1. You will loose money: 1-p-q

------

- Sample Space of X: flipping 2 coins: HH, HT, TH, TT
- At least one head (A) : A is subset of X ,
- P_A: belif of event A.

Bayesian pProbabilitic Modeling

Can't fo ML without assumptions: 
- how data is generated. 
ex: cat dog classification, there exist some underlying rules we don't know. we want to infer underlying mapping from images to labels. 

ex2: Gaussian density estimation: I give you 5 points and you want to infer /mean 

Given points: 0, 0.7, 1, 1.2, 1.3 , 2.1  what is the prob that mu is 10 generated my data? It is very unlikely!

In Bayesian Proba Modelling we watn to represent our beliefs/assumptions about how data was generated explicitly. Here are the asuumptions: 
- someone selected prarmaters: mu*, sigma*
- generated N data points: x_n ~ N/mu*, sigma2*)
- Gave us data = {x1, x2, x3...}


prior belief: what I believe params might look like. 
likelihood: how I believe data was generated given params
we will update the prior belief on "mu" conditioned on data you give me.  

--------------------

Bayesian Rule:

Give data what is the prob of mu=? given mu what is the prob of data (likelihood) * prob of mu (prior) / prob of data (evidence) 

<img src="assets/images_academicstudies/bayes_1.jpg" width="128"/>

Note: ss from [lecture - YouTube](https://www.youtube.com/watch?v=G6tUZRHnJYc&t=941s)

If you try to maximize the likelihood, mu = 0, sigma = 0. It doesn't make sense. It is Mazmum Likelihood failure. 

Tka e multiple datapoints. Take pdf each of them  and multiply all of them. 

    
      NOTATION
    Notation used in the slides:
    N - number of training points
    xn - index of training point
    Q - input dimensionality
    D - output dimensionality
    C - number of classes in classification
    K - number of units (neurons), often in last layer
    X - training inputs (N by Q matrix)
    x - single training input (Q by 1 vector)
    y - single training output (D by 1 vector)
    D = {(x1, y1), ..,(xN, yN)} = X, Y - training set
    W - neural network weight matrix (often last layer, often a random variable)
    theta - variational parameters

-------------------------

Bayesian Linear Regression: 

What we want is to find dist over W given D. 

## Articles that I've Read: 

- [Sleeper Agents: Training Deceptive LLMs that Persist Through Safety Training](https://arxiv.org/abs/2401.05566)

- [Question Decomposition Improves the Faithfulness of Model-Generated Reasoning](https://arxiv.org/abs/2307.11768)

- [Measuring Faithfulness in Chain-of-Thought Reasoning](https://arxiv.org/abs/2307.137029)

- [Semantic Uncertainty: Linguistic Invariances for Uncertainty Estimation in Natural Language Generation](https://arxiv.org/abs/2302.09664)

- [CLAM: Selective Clarification for Ambiguous Questions with Generative Language Models](https://arxiv.org/abs/2212.07769)

- [Managing AI Risks in an Era of Rapid Progress](https://arxiv.org/abs/2310.17688)

If managed carefully AI will help: cure diseases, improve live standards, protect ecosystem. On the other hand we can loose control of autonomus AI  systems. Large scale cyber crime, scoial manipulatin can happen. 
The harms such as misinformation & discrimination are already exist. It is vital to adress ongoing harms and emerging risks. 
We fdon't know how to  make The autonomus AI system safe. And it is open to misuse. We can solve today's tech. challenges: 

    - Oversight and honesty
      - Robustness: ai behave unpredictable in new situations. 
      - Interpretability and transperancy: we need to understand thier inner workings. 
      - Inclusive IA development: AI needs methods to mitigate biases and integrate value sof the many populationss it will affect. 
      - Risk evaluations: Better evalutio is needed. 
      - Addressing emerging challenges: AI need to have shutdown mechanism. 


- [AI Poses Doomsday Risks—But That Doesn’t Mean We Shouldn’t Talk About Present Harms Too](https://time.com/6303127/ai-future-danger-present-harms/)

        Notes: 
        "First, the public currently has little to no say over what models are built and how they are deployed.those most 
        affected by welfare systems have had little say in their automation. 
         
        Second, a strong auditing regime, where independent third-parties would scrutinize the practices and development 
        processes of AI labs, would help reduce risks overall. 
  
        Third, we should require meaningful human oversight of critical AI decisions, and avoid very-high-risk use cases such 
        as lethal autonomous weapons. 
  
        Fourth, we should rebalance the  funding going into AIs and urge companies to spend less on making them smarter 
        while increasing funding into making them safer, more transparent, and studying their social impacts. "

- [Thousands of AI Authors on the Future of AI](https://arxiv.org/abs/2401.02843)

      Notes: 
      2,778 researchers were surveyed who had published in top-tier artificial
      intelligence (AI) venues, asking for their predictions on the pace of AI progress and the nature and
      impacts of advanced AI systems. 
      
      "We defined High-Level Machine Intelligence (HLMI) thus:
      High-level machine intelligence (HLMI) is achieved when unaided machines can accomplish every
      task better and more cheaply than human workers. Ignore aspects of tasks for which being a human
      is intrinsically advantageous, e.g. being accepted as a jury member. Think feasibility, not adoption"
      
      “Full Automation of Labor” (FAOL).
      
        
      HLMI and FAOL are quite similar: FAOL asks about the automation of all occupations; HLMI asks about the
      feasible automation of all tasks.Predictions for a 50% chance of the arrival of FAOL are consistently more than sixty 
      years later than those for a 50%
      chance of the arrival of HLMI. 
        
      What causes AI progress?
      1) researcher effort, 2) decline
      in cost of computation, 3) effort put into increasing the size and availability of training datasets, 4) funding, and 5)
      progress in AI algorithms.
        
      Explainability:
      Most respondents considered it unlikely that users of AI systems in 2028 will be able to know the true
      reasons for the AI systems’ choices, with only 20% giving it better than even odds.
        
      Amount of concern potential scenarios deserve, organized from most to least extreme concern:
      Less concern on "Near full automation of labor makes people struggle to find meaning in their lives" and most concern on 
      AI makes it easy to spread false information. 
        
      How much should society prioritize AI safety research, relative to how much it
      is currently prioritized?  70% of respondents thought AI safety research should be prioritized more than it currently is.
      Examples of AI safety research might include:
      • Improving the human-interpretability of machine learning algorithms for the purpose of improving the safety and robustness of AI systems, not focused on improving AI capabilities
      • Research on long-term existential risks from AI systems
      • AI-specific formal verification research
      • Policy research about how to maximize the public benefits of AI
      • Developing methodologies to identify, measure, and mitigate biases in AI models to ensure fair
      and ethical decision-making

- [In-Context Learning Learns Label Relationships but Is Not Conventional Learning](https://arxiv.org/abs/2307.12375)


    In this paper, we provide novel insights into how ICL leverages label information, revealing both
    capabilities and limitations.
  
    - we study probabilistic aspects of ICL predictions and thoroughly examine the dynamics of ICL as more examples are provided. 
      - Our experiments show that:
        - ICL predictions almost always depend on in-context labels and that ICL can earn truly novel tasks in-context. 
        - ICL struggles to fully overcome prediction preferences acquired from pre-training data and, further, that ICL does not consider all in-context information equally.


This passage discusses the concept of in-context learning (ICL) in Large Language Models (LLMs) as demonstrated by 
various studies. Unlike traditional methods that involve updating the model's parameters (e.g., through gradient-based 
finetuning), ICL allows LLMs to learn from new examples without needing parameter adjustments. This is achieved by 
appending examples of the task to be learned directly to the input query. This method, particularly in its few-shot 
variant, has been widely adopted for enhancing performance across a range of natural language processing tasks.
However, the underlying reasons for ICL's effectiveness remain debated. Some researchers argue that ICL's success may be 
attributed to it simulating general-purpose learning algorithms, such as Bayesian inference or gradient descent. 
In contrast, others point out limitations, suggesting that LLMs don't actually "learn" in the anticipated manner during 
ICL, especially concerning grasping new task-specific input-label relationships.

The findings from the experiments reveal several key insights:

ICL and In-Context Labels: ICL does consider the labels of in-context examples, as shown by the reaction of probabilistic 
metrics to randomized labels and tests on novel tasks unknown to the LLMs from their pre-training.
Overcoming 

Pre-training Preferences: The study indicates that ICL struggles to overcome biases from pre-training data, 
with performance plateauing when in-context label relations conflict with pre-trained preferences. While additional 
prompting can somewhat mitigate this, it does not fundamentally alter the outcome.

Equitable Treatment of In-Context Information: The research further demonstrates that ICL does not treat all in-context 
information uniformly. Particularly, it preferentially utilizes information that is closer to the query, revealing an 
inherent bias in how LLMs process in-context data.


    - We  have shown that ICL is both better and worse than expected. 
    - On the one hand our results demonstrate that, against expectations set by prior work, ICL does incorporate in-context
    label information and can even learn truly novel tasks in-context. 
    - On the other hand, we have shown that analogies between ICL and conventional learning algorithms fall short in a variety of ways.
    In particular, label relationships inferred from pre-training have a lasting effect that cannot be sur-
    mounted by in-context observations. Additional prompting can improve but likely not overcome this
    deficiency. 
    - Further, ICL does not treat all information provided in-context equally and preferentially
    makes use of label information that appears closer to the query

Related literature with [the article](https://arxiv.org/abs/2307.12375) In-Context Learning Learns Label Relationships but Is Not Conventional Learning:

Ref1: https://www.hopsworks.ai/dictionary/in-context-learning-icl#:~:text=In%2Dcontext%20learning%20(ICL)%20learns%20a%20new%20task%20from,objective%20of%20next%20token%20prediction.
      
    Notes for Ref1:
    "In-context learning (ICL) is a specific method of prompt engineering where demonstrations of the task are provided to 
    the model as part of the prompt (in natural language). With ICL, you can use off-the-shelf large language models (LLMs) 
    to solve novel tasks without the need for fine-tuning. ICL can also be combined with fine-tuning for more powerful LLMs.
    LLMs that are large enough have shown a new type of machine learning - in-context learning -  the ability to learn to 
    solve new tasks by providing “training” examples in the prompt. In contrast to the aforementioned types of ML, the newly 
    learnt skill is forgotten directly after the LLM sends its response  - model weights are not updated. 
  
     One way to implement this service would be with prompts prefixed with example recipes before your text with your 
     available ingredients is finally added to the prompt. 
     
    For this, you may have thousands of recipes indexed in a VectorDB. When the query arrives, you use the ingredients to 
    look up the most relevant recipes in the VectorDB, then paste them in at the start of the prompt, and then write the 
    list of available ingredients, and finally, ask your LLM to generate a prompt. This is an example of retrieval-augmented generation for LLMs." [1]

Ref2 : [Lost in the Middle: How Language Models Use Long Contexts](https://arxiv.org/abs/2307.03172)

    Notes for Ref2:
    "We find that performance can degrade significantly when changing the position of relevant information, indicating that 
    current language models do not robustly make use of information in long input contexts. In particular, we observe that 
    performance is often highest when relevant information occurs at the beginning or end of the input context, and 
    significantly degrades when models must access relevant information in the middle of long contexts, even for explicitly long-context models."

Ref3: [An Explanation of In-context Learning as Implicit Bayesian Inference](https://arxiv.org/pdf/2111.02080.pdf)

    Notes for Ref3:
    "In this paper, we introduce a simple pretraining distribution where in-context learning emerges.
    To generate a document, we first draw a latent concept θ, which parameterizes the transitions of a
    Hidden Markov Model (HMM) (Baum and Petrie, 1966), then sample a sequence of tokens from the
    HMM (Figure 9)."



- [Attention Is All You Need](arXivpreprintarXiv:1706.03762,2017), Vaswani, A., Shazeer, N., Parmar, N., Uszkoreit, J., Jones, L., Gomez, 
  A. N., Kaiser, L., Polosukhin, I.
