---
jupyter:
  jupytext:
    notebook_metadata_filter: all
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.14.1
  kernelspec:
    display_name: Python 3 (ipykernel)
    language: python
    name: python3
  language_info:
    codemirror_mode:
      name: ipython
      version: 3
    file_extension: .py
    mimetype: text/x-python
    name: python
    nbconvert_exporter: python
    pygments_lexer: ipython3
    version: 3.8.0
  plotly:
    description: How to make scatter plots in Python with Plotly.
    display_as: basic
    language: python
    layout: base
    name: Scatter Plots
    order: 1
    page_type: example_index
    permalink: python/line-and-scatter/
    redirect_from: python/line-and-scatter-plots-tutorial/
    thumbnail: thumbnail/line-and-scatter.jpg
---

## What is Temperature?

The definition on OpenAI [1]

    The sampling temperature, between 0 and 1. 
    Higher values like 0.8 will make the output more random, 
    while lower values like 0.2 will make it more focused and deterministic. 

    If set to 0, the model will use log probability to automatically increase the 
    temperature until certain thresholds are hit.

In Cohere, the temperature example is between 0.5 and 5. And in [this](https://txt.cohere.com/llm-parameters-best-outputs-language-ai/) blog 
there are really nice examples. 

Temperature is a parameter which is added to softmax function, it changes the output probabilities. It helps us to control the creativeness of a Large Language Model.

This is the original softmax function: 

<div class="fig figcenter fighighlight">
  <img src="/assets/images/softmax.PNG" width="50%">
  <div class="figcaption">softmax</div>
</div>


When we add Temperature parameter: 

<div class="fig figcenter fighighlight">
  <img src="/assets/images/softmax_temp.PNG" width="50%">
  <div class="figcaption">softmax with temperature</div>
</div>

Here, zj is the output of the neural network. There may be a lot of forward pass, some activation functions, but as a result it is a floating number. 

- As Temperature approaches 0, the output probabilities become more "sharp". One of the element will be close to 1.
- As Temperature increases, the output probabilities become more "flat" or "uniform", reducing the difference between the probabilities of different elements.

If we want repetitive answer, no creativity at all, we can decrease the Tempereature. If we want more creative answers, we can increase it.

-----------------------------------------------------

This is an example. Let's imagine our corpus has only 5 words: 

The prediction of next token of given sentence: "At the table, there is a delicious" will be one of the words in the corpus. 
These are the original results: 

<div class="fig figcenter fighighlight">
  <img src="/assets/images/softmax_df.PNG" width="50%">
  <div class="figcaption">Output probabilities with softmax</div>
</div>

You can try different temperature values to see how the output changes:

{% include temperature_slider.html %}


# References
[1] https://platform.openai.com/docs/api-reference/audio/createTranscription#audio/createTranscription-temperature
[2] https://txt.cohere.com/llm-parameters-best-outputs-language-ai/#:~:text=one%20long%20burst.-,Temperature,-Temperature%20is%20a



