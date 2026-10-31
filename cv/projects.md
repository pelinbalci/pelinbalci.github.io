# Projects tab — each "## " heading is one project, shown in this order.
# Lines right under the heading: kind (small grey label), stack, link (button text), url.
# Leave "url" empty for client work you can't link to — the button is hidden.

## Information extraction from pathology reports
kind: Research · NLP
stack: Transformers · NER
link: Paper
url: https://drive.google.com/file/d/1l9rPr03DtO9mIvyQzE9H3jETMRFofcw/view

Structuring free-text pathology reports with NLP. [dataset, method, headline result]

## Delivery and shift optimization for a fast-food chain
kind: Optimization · Client work
stack: Python · SimPy · Gurobi · SQL
link:
url:

Built a SimPy simulation of the delivery process (order assignment and delivery times) to model the current state. Calculated hourly driver targets from order distributions, then assigned full- and part-time shifts with a Gurobi model that minimizes the gap between target and assigned drivers. The new shifts were validated in the simulation before the live test. [result: e.g. delivery time or late deliveries before → after]

## Day-ahead energy imbalance direction prediction
kind: ML in production · Client work
stack: PyTorch · Databricks · SQL · Power BI
link:
url:

Predicts the hourly system imbalance direction for the next day for an energy company, using public EPİAŞ Transparency Platform data. Neural network in PyTorch, deployed on Databricks with weekly retraining and an automated prediction email to the customer. [result: e.g. accuracy vs. baseline, how long it ran]

## Occupancy detection on a microcontroller
kind: TinyML
stack: TensorFlow Lite · Neuton AI
link: GitHub
url: https://github.com/pelinbalci/Tinyml_Occupancy_Detection

On-device occupancy classifier, compared across TensorFlow Lite and Neuton AI.

## Audio and motion classifiers
kind: TinyML
stack: Edge Impulse
link: Write-ups
url: https://pelinbalci.com/tinyml/2022/01/17/Audio-Classifier.html

Two embedded classifiers built end-to-end with Edge Impulse, with write-ups.

## Movie recommendation
kind: Live app
stack: Python · Streamlit
link: Open app
url: https://pelinbalci-movierecommendation.streamlit.app/

Recommender system deployed as an interactive web app.

## EasyOCR and language detection
kind: Live app
stack: Hugging Face Spaces
link: Spaces
url: https://huggingface.co/pelinbalci

Two Hugging Face Spaces for text extraction and language identification.

## Tiny AI World
kind: This site
stack: D3.js · Python · GitHub Pages
link: GitHub
url: https://github.com/pelinbalci/pelinbalci.github.io

Interactive knowledge graph of my learning notes, generated from Markdown.
