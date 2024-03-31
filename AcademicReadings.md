---
layout: page
title: Academic Studies
permalink: /Academic Studies/
---

## Lectures
- [Yarin Gal -. Bayesian Deep Learning](https://www.youtube.com/watch?v=G6tUZRHnJYc&t=941s)

**Bayesian Probability Theory - the Language of Ucertainty:**
- Would you pay a penny (0.01 pound) to buy a note where I commit to paying 1 pound instead?
- Would you pay a penny (0.99pound) to buy a note where I commit to paying 1 pound instead? 
- Would you sell a unit wager at p for heads? Yu get p and you have to pay 1 pound if head.

I think he expected outcome will be 0.5 heads. Which means 0.5*1*note It need to be less than p*1*note for buyer and higher than p*1*note for seller. 




## Articles that I've Read: 
- [Attention Is All You Need](arXivpreprintarXiv:1706.03762,2017), Vaswani, A., Shazeer, N., Parmar, N., Uszkoreit, J., Jones, L., Gomez, 
  A. N., Kaiser, L., Polosukhin, I.


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


