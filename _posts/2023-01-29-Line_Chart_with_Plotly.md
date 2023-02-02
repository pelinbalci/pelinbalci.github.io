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


# How to embed plotly chart to md file?

I used jupyter notebook. After plotting the chart, it is saved under _posts with the code below. 

```python
import plotly.express as px
import plotly.io as pio
fig = px.line(df, x="Date", y="Sales", title='Daily Sales')
fig.show()
pio.write_html(fig, file='plotly_simple.html', auto_open=False)
```

I moved them to _includes folder. And then, I created an md file which you are reading now, and add a line 
to show the plot: 

```{% include plotly_simple.html %}```

# References
- https://raw.githubusercontent.com/plotly/plotly.py/master/doc/python/line-and-scatter.md
- https://stackoverflow.com/questions/60513164/display-interactive-plotly-chart-html-file-on-github-pages
- https://stackoverflow.com/questions/64241461/plotly-how-to-add-markers-at-specific-points-in-plotly-line-graph-python-pan
- https://stackoverflow.com/questions/68731627/plotly-express-line-chart-mark-specific-points-and-retain-hover-data
- https://davistownsend.github.io/blog/PlotlyBloggingTutorial/