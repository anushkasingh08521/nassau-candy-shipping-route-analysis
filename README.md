# \# Factory-to-Customer Shipping Route Efficiency Analysis

# 

# \## 📦 Project Overview

# 

# This project analyzes shipment data from Nassau Candy Distributor to evaluate factory-to-customer shipping route efficiency across different regions and states.

# 

# The analysis focuses on shipping lead time, route performance, delays, geographic patterns, and shipping modes to identify routes and locations that may require further operational investigation.

# 

# An interactive Streamlit dashboard was developed to allow users to explore the results through filters and visualizations.

# 

# \---

# 

# \## 🎯 Business Problem

# 

# Nassau Candy Distributor ships products from multiple factories to customers across different geographic regions.

# 

# The objective of this project is to understand:

# 

# \- Which factory-to-customer routes handle high shipment volumes

# \- Which routes have higher average shipping lead times

# \- Where delayed shipments are more frequent

# \- How shipping performance varies across states and regions

# \- How different shipping modes compare in terms of lead time and delay patterns

# 

# \---

# 

# \## 📊 Dataset

# 

# The dataset contains \*\*10,194 shipment records\*\* with information including:

# 

# \- Order Date

# \- Ship Date

# \- Ship Mode

# \- Customer Location

# \- Region

# \- Product

# \- Sales

# \- Units

# \- Gross Profit

# \- Cost

# 

# Additional factory information was incorporated to create factory-to-customer route analysis.

# 

# \---

# 

# \## 🔍 Analysis Performed

# 

# The project includes:

# 

# \- Data cleaning and validation

# \- Shipping lead-time calculation

# \- Route-level analysis

# \- Factory-to-state route analysis

# \- Regional analysis

# \- State-level analysis

# \- Ship-mode comparison

# \- Delay analysis

# \- Route variability analysis

# \- Route efficiency scoring

# \- Geographic visualization

# \- Interactive dashboard development

# 

# \---

# 

# \## 🚚 Key Metrics

# 

# \### Shipping Lead Time

# 

# Shipping lead time was calculated as:

# 

# `Ship Date - Order Date`

# 

# \### Delay Rate

# 

# A shipment was classified as delayed when its shipping lead time exceeded the dataset median of \*\*1,274 days\*\*.

# 

# This threshold is a project-specific analytical threshold and does not represent an official logistics SLA.

# 

# \### Route Efficiency Score

# 

# A relative route efficiency score was calculated using min-max normalization of route-level average lead time.

# 

# Higher scores indicate relatively lower average lead times within the analyzed routes.

# 

# \---

# 

# \## 📈 Dashboard



# ![Nassau Candy Distributor Streamlit Dashboard](images/dashboard_screenshot.png)



# The Streamlit dashboard contains four main sections:

# 

# \### 📊 Overview

# \- Shipment KPIs

# \- Route performance

# \- Lead-time analysis

# \- Route efficiency visualization

# 

# \### 🗺️ Geography

# \- State-level shipping analysis

# \- Geographic distribution

# \- Regional comparisons

# 

# \### 🚚 Ship Modes

# \- Shipping volume by mode

# \- Average lead time

# \- Delay patterns

# \- Cost and performance comparison

# 

# \### 🔎 Route Drill-Down

# \- Factory-to-state route analysis

# \- Shipment volume

# \- Average lead time

# \- Delay rate

# \- Route-level performance

# 

# Interactive filters allow users to explore the data by:

# 

# \- Region

# \- State

# \- Ship Mode

# \- Order Date

# \- Lead-time threshold

# 

# \---

# 

# \## 🛠️ Technologies Used

# 

# \- \*\*Python\*\*

# \- \*\*Pandas\*\*

# \- \*\*Plotly\*\*

# \- \*\*Streamlit\*\*

# \- \*\*Jupyter Notebook / Google Colab\*\*

# \- \*\*GitHub\*\*

# 

# \---

# 

# \## 📁 Project Structure

# 

# ```text

# Nassau Candy Shipping Route Analysis/

# │

# ├── app.py

# ├── dashboard\_data.csv

# ├── requirements.txt

# ├── README.md

# ├── .gitignore

# └── .gitattributes

