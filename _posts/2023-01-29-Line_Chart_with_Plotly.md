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
    description: How to use mark and annotation in plotly line charts 
    display_as: basic
    language: python
    layout: base
    name: Line Charts
    order: 1
    page_type: example_index
    permalink: python/line/
    redirect_from: python/line-plots/
    thumbnail: thumbnail/line.jpg
---

In this file I will explain how to use plotly with markers and annotation. It is very easy to plot chart in plotly express!:)

Let's create two datasets: they include sales & anomalies for the first 10 days of Jan 2023. 

```python
# create dataset
import pandas as pd
df = pd.DataFrame({"Date": ["2023-01-01", "2023-01-02", "2023-01-03", "2023-01-04", "2023-01-05", "2023-01-06", "2023-01-07", 
              "2023-01-08", "2023-01-09", "2023-01-10"],
     "Analysis": ["Normal", "Anomaly", "Normal", "Anomaly", "Anomaly", "Normal", "Normal", "Normal", "Normal", "Normal"],
     "Sales": [120, 30, 115, 10, 5, 100, 99, 123, 134, 96]})

df_with_group = pd.DataFrame({
    "Date": ["2023-01-01", "2023-01-02", "2023-01-03", "2023-01-04", "2023-01-05", "2023-01-06", "2023-01-07", 
             "2023-01-08", "2023-01-09", "2023-01-10", "2023-01-01", "2023-01-02", "2023-01-03", "2023-01-04", 
             "2023-01-05", "2023-01-06", "2023-01-07", "2023-01-08", "2023-01-09", "2023-01-10"],
    "Analysis": ["Normal", "Anomaly", "Normal", "Anomaly", "Anomaly", "Normal", "Normal", "Normal", "Normal", "Normal",
                 "Anomaly", "Normal", "Normal", "Anomaly", "Anomaly", "Normal", "Normal", "Normal", "Normal", "Anomaly"],
    "Sales": [120, 30, 115, 10, 5, 100, 99, 123, 134, 96, 
              15, 100, 103, 13, 8, 88, 111, 126, 120, 25],
    "Sales_Group": ["A", "A", "A", "A", "A", "A", "A", "A", "A", "A", "B", "B", "B", "B", "B", "B", "B", "B", "B", "B"]
})
```

We need to convert the "date" to datetime to show it in x axis properly. 

```
# to datetime
df.Date = pd.to_datetime(df.Date)
df_with_group.Date = pd.to_datetime(df_with_group.Date)
```

Here is a simple way to plot a animation chart!

```python
import plotly.express as px
fig = px.line(df, x="Date", y="Sales", title='Daily Sales')
fig.show()
```

{% include plotly_simple.html %}

If we want to see 2 sales group's performance together:

```python
fig2 = px.line(df_with_group, x="Date", y="Sales", color='Sales_Group', title='Daily Sales')
fig2.show()
```

{% include_relative plotly_simple_2.html %}

Let's put them together and see 2 group's sales performance: 

### How to embed plotly chart to md file?

It is a bit tricky when you want to pusblish your plotly express plots as md file. In this blog I'm using Jeykll and mostly, I prefer
to convert my jupyter notebooks to html and publish them directly. However, when it comes to publish plotly there are many erros 
in github deployment. 

One error example: 

```
Liquid syntax error (line 15038): Variable '{{ x.observe(notebook Container, {childList: true}' was not properly terminated with regexp: /\}\}/ in /github/workspace/_posts/2023-01-10-Line_Chart_with_Plotly.html

```

First I tried to solve this problem by my own with this function:

```python
def prepend_string(filename, string):
    with open(filename, 'r+') as f:
        content = f.read()
        f.seek(0, 0)
        f.write(string.rstrip('\r\n') + '\n' + content)
        f.seek(15038, 0)
        f.write(string.replace("}", "}}"))
        f.seek(13617, 0)
        f.write(string.replace("}", "}}"))
        f.seek(13611, 0)
        f.write(string.replace("}", "}}"))
```

Unfortunately the error continues with new lines. I know this is not the true way to deal with html files, but I try anyway:)

Then I gave up converting jupyter to html, instead I decided to create an md file which you're reaaing now:)

I used jupyter notebook to plot and save the cahrts. Saving plotly express as html file:

```python
import plotly.express as px
import plotly.io as pio
fig = px.line(df, x="Date", y="Sales", title='Daily Sales')
fig.show()
pio.write_html(fig, file='plotly_simple.html', auto_open=False)
```

I moved those html files to _includes folder. In order to show the plot in the md file you can simply add a line:
        
```html
{% include plotly_simple.html %}
```


### References
- https://raw.githubusercontent.com/plotly/plotly.py/master/doc/python/line-and-scatter.md
- https://stackoverflow.com/questions/60513164/display-interactive-plotly-chart-html-file-on-github-pages
- https://stackoverflow.com/questions/64241461/plotly-how-to-add-markers-at-specific-points-in-plotly-line-graph-python-pan
- https://stackoverflow.com/questions/68731627/plotly-express-line-chart-mark-specific-points-and-retain-hover-data
- https://davistownsend.github.io/blog/PlotlyBloggingTutorial/