---
title: "Temperature"
id: "temperature"
category: "genai"
tags: ["temperature", "llm", "video"]
related: ["configuration"]
date: "2025-11-08"
description: "A brief description of temperature parameter"
---

# Temperature 

**Temperature** is a parameter which is injected into the **softmax function**, enabling the users to manipulate the 
output probabilities. It helps us to control the **creativeness** of a Large Language Model.

The range of the temperature parameter is defined as 0 and 1 in OpenAI documentation. In the context of Cohere, 
temperature values fall within the range of 0 to 5. _See the references below._

-----------------------------------------------------

This is the original softmax function: 

<div class="fig figcenter fighighlight">
  <img src="/assets/image_assets/temperature_images/softmax.PNG" width="50%">
  <div class="figcaption"> </div>
</div>


When we add Temperature parameter:

<div class="fig figcenter fighighlight">
  <img src="/assets/image_assets/temperature_images/softmax_temp.PNG" width="50%">
  <div class="figcaption"> </div>
</div>

Remember that zj is the output of the neural network: it is a floating number. If you want to learn more about 
softmax function, read [here](https://github.com/pelinbalci/Intro_Deep_Learning/blob/master/Intro_NN/notes/1_Perceptron_math.md#multiclass-classification--softmax:~:text=Multiclass%20Classification%20%26%20Softmax).

-----------------------------------------------------

- As Temperature approaches 0, the output probabilities become more "sharp". One of the probability will be close to 1.
- As Temperature increases, the output probabilities become more "flat" or "uniform", reducing the difference between the probabilities of different elements.

If we want repetitive answers, and no creativity at all, we can decrease the Temperature. If we want more creative answers, we can increase it.

-----------------------------------------------------

# Example 

Let's imagine that our corpus has only 5 words: ["donut", "cake", "apple", "juice", "book"]

The prediction of next token of given sentence: "At the table, there is a delicious" will be one of the words in the corpus. 

These are the original results: 

<div class="fig figcenter fighighlight">
  <img src="/assets/image_assets/temperature_images/softmax_df.PNG" width="50%">
  <div class="figcaption"> </div>
</div>

You can try different temperature values to see how the output changes.

<div>
<iframe 
    src="https://www.pelinbalci.com/assets/components/temperature_slider.html" 
    width="100%" 
    height="600" 
    style="border:none;"
></iframe>
</div>

Listen my YouTube Vide from [here](https://youtu.be/KbUPOJ8Fmzs)

Happy Learning! :)

# References
- [1] https://platform.openai.com/docs/api-reference/audio/createTranscription#audio/createTranscription-temperature
- [2] https://txt.cohere.com/llm-parameters-best-outputs-language-ai/
- [3] https://peterchng.com/blog/2023/05/02/token-selection-strategies-top-k-top-p-and-temperature/
