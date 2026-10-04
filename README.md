# 📊 E-Commerce Pricing and Demand Analysis

An interactive **Data Science and Business Analytics project** that analyzes e-commerce sales, product demand, pricing behavior, price elasticity, competitor pricing, and inventory requirements through an interactive Streamlit dashboard.

## 🚀 Project Overview

E-commerce businesses need to understand product demand, pricing behavior, competition, and inventory requirements to make better business decisions.

This project analyzes historical e-commerce data and converts the analysis into practical business insights using Python, Pandas, data visualization, demand prediction, pricing analysis, and Streamlit.

The project contains separate analytical pipelines for:

- Demand and sales analysis
- Demand prediction
- Pricing analysis
- Price elasticity analysis
- Competitor pricing analysis
- Business insights
- Inventory recommendations

## 🎯 Objectives

The main objectives of this project are:

- Analyze historical e-commerce sales data
- Understand product-level demand patterns
- Identify top-performing products
- Analyze sales and revenue trends
- Study product pricing behavior
- Compare product prices with competitors
- Measure price elasticity
- Predict next-month product demand
- Calculate suggested stock using a safety buffer
- Identify prediction risk
- Generate business-oriented recommendations

## ✨ Key Features

### 🏠 Dashboard

Provides an overview of important e-commerce metrics and analytical modules.

### 📤 Upload Data

Users can upload their own CSV sales dataset.

The application automatically detects commonly used column names for:

- Date
- Product
- Quantity
- Price

The uploaded data is validated and transformed before analysis.

### 📦 Demand Analysis

Analyze:

- Sales trends
- Product demand
- Units sold
- Revenue
- Monthly demand
- Top products
- Product-level performance
- Sales summary by product
- Product transaction details

### 🔮 Demand Prediction

The application provides a baseline next-month demand estimate for a selected product using recent historical monthly demand.

It provides:

- Predicted Demand
- Safety Buffer
- Suggested Stock
- Historical vs predicted demand visualization

A **10% safety buffer** is used as a baseline inventory recommendation.

> The prediction is an analytical baseline and should not be considered a guaranteed future demand value.

### 💰 Pricing Analysis

Analyze:

- Product prices
- Quantity sold
- Price changes
- Price gaps
- Competitor prices
- Competitive position
- Pricing trends

### 📉 Price Elasticity

Price elasticity is analyzed to understand the relationship between changes in price and quantity sold.

Products are classified as:

- Elastic
- Inelastic
- Unit Elastic

The project also considers the number of observations when evaluating elasticity reliability.

> The analysis is observational and does not establish a causal relationship between price and demand.

### 🏪 Competitor Analysis

Products are compared with competitor prices and classified as:

- Below Competitors
- Similar to Competitors
- Above Competitors

This helps identify products that may require pricing attention.

### 💡 Business Insights

The project converts analytical results into business-oriented insights related to:

- Demand
- Pricing
- Competition
- Inventory
- Prediction risk
- Product performance

## 📊 Datasets

The project uses two separate datasets for different analytical purposes.

### 1. Retail Price Dataset

Used for:

- Pricing analysis
- Competitor analysis
- Price elasticity
- Price changes
- Competitive positioning

### 2. Online Retail II Dataset

Used for:

- Sales analysis
- Demand analysis
- Demand prediction
- Inventory recommendations

The datasets are kept separate because they support different analytical objectives.

## 🧹 Data Cleaning

The Online Retail II dataset was processed through multiple cleaning steps, including:

- Invoice date conversion
- Cancellation handling
- Invalid quantity removal
- Invalid price removal
- Special transaction removal
- Duplicate removal
- Missing-value analysis
- Data validation

The cleaned dataset is stored in:

```text
data/processed/online_retail_clean.csv
```

## ⚙️ Feature Engineering

### Demand Features

The demand analysis pipeline creates the following time-based features:

- Year
- Month
- Day
- Day of Week
- Hour
- Weekend Indicator

These features help identify temporal patterns in product demand.

### Pricing Features

The pricing analysis pipeline creates features including:

- Month
- Year
- Quarter
- First-Half Indicator
- Second-Half Indicator
- Average Competitor Price
- Minimum Competitor Price
- Maximum Competitor Price
- Price Difference
- Price Gap Percentage
- Price Change
- Price Change Percentage
- Quantity Change Percentage
- Price Elasticity
- Competitive Position

## 📈 Demand Prediction

The project provides a baseline next-month demand prediction for products.

The prediction workflow is:

```text
Historical Sales Data
        ↓
Monthly Demand Aggregation
        ↓
Recent Demand Analysis
        ↓
Next-Month Demand Estimate
        ↓
10% Safety Buffer
        ↓
Suggested Stock
```

For uploaded datasets, the application analyzes the recent monthly demand of the selected product and calculates a baseline estimate for the following month.

> Demand prediction is intended for analytical and planning purposes and should not be considered a guaranteed forecast.

## 📦 Inventory Recommendation

The application converts predicted demand into a simple inventory recommendation.

A **10% safety buffer** is applied to the predicted demand.

```text
Safety Stock = Predicted Demand × 10%

Suggested Stock = Predicted Demand + Safety Stock
```

The suggested stock value provides an additional buffer to help reduce the risk of insufficient inventory.

## 📉 Price Elasticity Methodology

Price elasticity measures the relationship between percentage changes in price and percentage changes in quantity sold.

The basic formula used is:

```text
Price Elasticity =
% Change in Quantity / % Change in Price
```

The project performs product-level elasticity analysis and uses the median elasticity value to reduce the influence of extreme observations.

Products are classified into:

- Elastic
- Inelastic
- Unit Elastic

The project also evaluates the number of observations available for each product to provide an indication of elasticity reliability.

> The elasticity analysis is observational and does not establish a causal relationship between price and demand.

## 🏪 Competitor Pricing Logic

The project compares product prices with competitor prices using the calculated price gap.

Products are classified using the following logic:

```text
Price Gap < -5
→ Below Competitors

Price Gap > 5
→ Above Competitors

Otherwise
→ Similar to Competitors
```

This classification helps identify products whose prices differ significantly from competitor prices.

## ⚠️ Prediction Risk Analysis

The demand prediction pipeline evaluates prediction reliability using prediction error.

Products are grouped into different risk categories:

- Low Risk
- Moderate Risk
- High Risk
- Zero Demand

The risk classification helps businesses identify predictions that may require additional attention before making inventory decisions.

The risk categories are based on relative prediction error:

```text
Low Risk
→ Relative Error ≤ 20%

Moderate Risk
→ Relative Error > 20% and ≤ 50%

High Risk
→ Relative Error > 50%

Zero Demand
→ Actual Demand = 0
```

> Prediction risk is intended as a decision-support indicator rather than a guarantee of future demand accuracy.

## 💡 Business Questions Answered

### 📦 Demand Analysis

- Which products have the highest demand?
- How does product demand change over time?
- Which products have strong sales performance?
- Which products may require additional inventory?

### 💰 Revenue Analysis

- Which products generate the highest revenue?
- How does revenue change over time?
- Which products contribute most to sales performance?

### 💵 Pricing Analysis

- How are products priced?
- How does price change over time?
- Which products have significant price gaps?
- How does quantity sold vary with price changes?

### 📉 Price Elasticity

- Which products are relatively price-sensitive?
- Which products are relatively less price-sensitive?
- Which products have more reliable elasticity estimates?

### 🏪 Competitor Analysis

- Which products are priced below competitors?
- Which products have similar prices to competitors?
- Which products are priced above competitors?

### 📦 Inventory Planning

- What is the estimated next-month demand?
- What safety stock should be considered?
- What is the suggested stock level?
- Which predictions have higher risk?

## 🛠️ Technologies Used

### Programming Language

- Python

### Data Analysis

- Pandas
- NumPy

### Data Visualization

- Matplotlib
- Streamlit

### Machine Learning

- Scikit-learn
- Gradient Boosting

### Development Tools

- Jupyter Notebook
- Visual Studio Code

### Version Control

- Git
- GitHub
- Git LFS

### Deployment

- Streamlit Community Cloud

## 📁 Project Structure

```text
E-Commerce Pricing and Demand Analysis/
│
├── app/
│   └── app.py
│
├── data/
│   ├── raw/
│   │   └── retail_price.csv
│   │
│   ├── processed/
│   │   ├── online_retail_clean.csv
│   │   ├── retail_price_features.csv
│   │   └── product_elasticity_summary.csv
│   │
│   └── predictions/
│       ├── next_month_demand_predictions.csv
│       ├── prediction_reliability.csv
│       ├── final_decision_table.csv
│       ├── prediction_risk_summary.csv
│       └── business_action_recommendations.csv
│
├── models/
│   ├── gradient_boosting_demand_model.pkl
│   ├── model_features.pkl
│   └── model_metrics.pkl
│
├── notebooks/
│   ├── data_understanding1.ipynb
│   ├── data_cleaning_2.ipynb
│   ├── EDA.ipynb
│   ├── feature_engineering.ipynb
│   ├── modeling_preparation.ipynb
│   ├── prediction_demo.ipynb
│   ├── pricing_analysis.ipynb
│   ├── pricing_feature_engineering.ipynb
│   └── business_insights.ipynb
│
├── requirements.txt
├── .gitignore
├── .gitattributes
└── README.md
```

## ⚙️ How to Run Locally

### 1. Clone the Repository

```bash
git clone https://github.com/sonychebrolu6/ecommerce-pricing-demand-analytics.git
```

### 2. Navigate to the Project Directory

```bash
cd ecommerce-pricing-demand-analytics
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Streamlit Application

On Windows:

```bash
py -m streamlit run app/app.py
```

Alternatively:

```bash
python -m streamlit run app/app.py
```

The Streamlit application will open in your default web browser.

## ☁️ Deployment

The application is designed to be deployed using **Streamlit Community Cloud**.

### Deployment Configuration

```text
Repository:
sonychebrolu6/ecommerce-pricing-demand-analytics

Branch:
main

Main Application File:
app/app.py
```

The project uses Git LFS for the large processed dataset.

## 📌 GitHub Repository

The complete source code, notebooks, data-processing outputs, model files, and application code are maintained in the GitHub repository:

https://github.com/sonychebrolu6/ecommerce-pricing-demand-analytics

## 🔮 Future Improvements

Possible future improvements include:

- Advanced time-series forecasting models
- More advanced demand forecasting
- Dynamic pricing recommendations
- Customer segmentation
- Product recommendation systems
- Real-time sales data integration
- Advanced inventory optimization
- Automated model retraining
- Model performance monitoring
- Geographic sales analysis
- Real-time business dashboards

## 👩‍💻 Author

**Sony Chebrolu**

B.Tech – Computer Science and Data Science

### Areas of Interest

- Data Analytics
- Data Science
- Machine Learning
- Business Intelligence
- Data Visualization

## 🔄 Project Workflow

```text
E-Commerce Data
       ↓
Data Cleaning
       ↓
Exploratory Data Analysis
       ↓
Feature Engineering
       ↓
Demand Analysis
       ↓
Demand Prediction
       ↓
Pricing Analysis
       ↓
Price Elasticity
       ↓
Competitor Analysis
       ↓
Business Insights
       ↓
Streamlit Dashboard
       ↓
Cloud Deployment
```

## ⭐ Project Highlights

This project demonstrates practical experience in:

- Data cleaning and preprocessing
- Exploratory Data Analysis
- Feature engineering
- Data visualization
- Demand analysis
- Demand prediction
- Pricing analytics
- Price elasticity analysis
- Competitor analysis
- Inventory recommendation
- Business intelligence
- Streamlit application development
- Machine learning
- Git and GitHub
- Git LFS
- Cloud deployment

## 📊 Conclusion

The **E-Commerce Pricing and Demand Analysis** project demonstrates how historical e-commerce data can be transformed into meaningful business insights.

By combining demand analysis, pricing analysis, price elasticity, competitor comparison, demand prediction, and inventory recommendations, the project provides a practical analytics workflow that can support better business decision-making.

The interactive Streamlit application makes these analytical results easier to explore and apply to both existing and uploaded sales datasets.
