---
layout: base
title: My Apps
permalink: /apps/
---

## The Markdown
We'll abuse some Markdown elements to get the layout we want. You can choose to style your page differently, but here we'll have code examples on the right, and code explanations on the left.

### First, we need to tell Markdown where the two column layout begins.
Anything before this element will be rendered normally.

```
<div class="begin-examples"></div>
```

And we should also tell it where the two column layout ends.

```
<div class="end-examples"></div>
```

### `h2` will be an example section header.

```
## Section title
```

And any text directly after the section title will not be split into two columns.



HuggingFace EasyOCR App
[![HuggingFace EasyOCR App](assets/hf_easyocr.png)](https://huggingface.co/spaces/pelinbalci/easyocr){:target="_blank"}

HuggingFace LanguageDetection App
[![HuggingFace LanguageDetection App](assets/hf_language_detect.png)](https://huggingface.co/spaces/pelinbalci/easyocr){:target="_blank"}

LanguageDetection App - Streamlit Cloud
[![HuggingFace LanguageDetection App](assets/hf_language_detect.png)](https://pelinbalci-streamlit-ml-app-main-q6mq7c.streamlit.app/){:target="_blank"}


