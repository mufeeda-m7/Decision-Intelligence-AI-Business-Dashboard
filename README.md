# 🧠 Decision Intelligence AI – Business Dashboard

An interactive Business Analytics and Machine Learning project that analyzes business performance, predicts product-level profit, identifies loss-making products, and provides data-driven recommendations to support better business decisions.

This project combines **Business Intelligence, Exploratory Data Analysis, Machine Learning, Decision Support Logic, and Interactive Data Visualization** into a unified dashboard.

---

## 📌 Project Overview

Business performance is not determined by sales alone. A product may generate high revenue but still result in a loss due to discounts, costs, or pricing decisions.

This project uses historical Superstore sales data to analyze business performance, identify potential losses, predict profit, and provide actionable business recommendations.

The dashboard provides an interactive environment where users can explore business KPIs, analyze sales performance, identify loss-making products, and simulate different discount scenarios to understand their impact on predicted profit.

## 🎯 Project Objectives

- Analyze historical sales and profit data to understand business performance.
- Track important business KPIs such as total sales, total profit, and profit margin.
- Explore sales performance across product categories and business regions.
- Identify products and orders that generate negative profit.
- Analyze the relationship between sales, quantity, discount, and profit.
- Develop a Machine Learning model to predict business profit.
- Generate automated business insights and decision recommendations.
- Simulate different discount scenarios to evaluate their impact on profit.
- Build an interactive dashboard for business performance monitoring and decision support.

---

## ✨ Key Features

### 1. 📊 Business Overview Dashboard

- Displays total sales and total profit.
- Calculates overall profit margin.
- Shows an overall business health score.
- Provides category-based and region-based filtering.
- Presents important business performance indicators in one place.

### 2. 📈 Sales Analytics

- Visualizes total sales across product categories.
- Compares profit performance across business regions.
- Identifies high-performing and low-performing business segments.
- Provides interactive charts for better business understanding.

### 3. 🚨 Loss-Making Product Analysis

- Identifies products and orders generating negative profit.
- Displays the most loss-making products.
- Shows product category, region, sales, profit, and discount information.
- Helps identify products that may require pricing or discount adjustments.

### 4. 🤖 Machine Learning-Based Profit Prediction

- Uses a trained Linear Regression model.
- Takes Sales, Quantity, and Discount as input features.
- Predicts estimated profit based on the supplied values.
- Loads the trained model from the `models/` directory.

### 5. 🎛️ Interactive Profit Simulator

- Allows users to select a product from the dataset.
- Uses historical median sales and quantity as the product baseline.
- Provides an adjustable discount percentage.
- Predicts estimated profit for the selected discount scenario.
- Displays business recommendations based on predicted profit.
- Calculates a scenario health score.

### 6. 💡 Automated Business Insights

Generates data-driven observations about:

- Overall business profit margin.
- Best-performing product categories.
- Weakest-performing product categories.
- Best-performing business regions.
- Weakest-performing business regions.
- Number of loss-making orders.
- Potential areas for improving business profitability.

### 7. 🧠 Decision Recommendations

The system generates recommendations based on predefined profit thresholds.

| Predicted Profit | Recommendation                         |
| ---------------- | -------------------------------------- |
| Above $500       | Highly Profitable – Increase Marketing |
| Above $0 to $500 | Profitable – Maintain Strategy         |
| -$500 to $0      | Low Profit – Reduce Discount           |
| Below -$500      | Loss – Stop Selling / Review Pricing   |

**Note:** These recommendations are generated using predefined business rules. They are not produced by a separate Generative AI model.

---

## 🛠️ Technologies Used

| Technology        | Purpose                                     |
| ----------------- | ------------------------------------------- |
| Python            | Core programming language                   |
| Pandas            | Data manipulation and analysis              |
| NumPy             | Numerical operations                        |
| Scikit-learn      | Machine Learning model development          |
| Linear Regression | Profit prediction                           |
| FastAPI           | Backend API development                     |
| Uvicorn           | Running the FastAPI application             |
| HTML              | Dashboard structure                         |
| CSS               | Dashboard styling                           |
| JavaScript        | Frontend interactions and API communication |
| Chart.js          | Interactive data visualization              |
| Matplotlib        | Exploratory data visualization              |
| Jupyter Notebook  | Data exploration and analysis               |
| Pickle            | Saving and loading the trained model        |
| Streamlit         | Additional dashboard implementation         |

---

## 📂 Dataset

The project uses a **Superstore Sales Dataset** containing approximately **9,994 records and 21 columns**.

The dataset contains information about orders, customers, products, locations, sales, discounts, and profits.

### Dataset Information

| Attribute          | Details |
| ------------------ | ------- |
| Total Records      | 9,994   |
| Total Columns      | 21      |
| Product Categories | 3       |
| Business Regions   | 4       |
| Unique Products    | 1,850   |
| Missing Values     | 0       |
| Duplicate Records  | 0       |

### Dataset Attributes

| Category             | Attributes                                         |
| -------------------- | -------------------------------------------------- |
| Order Information    | Row ID, Order ID, Order Date, Ship Date, Ship Mode |
| Customer Information | Customer ID, Customer Name, Segment                |
| Location Information | Country, City, State, Postal Code, Region          |
| Product Information  | Product ID, Category, Sub-Category, Product Name   |
| Business Metrics     | Sales, Quantity, Discount, Profit                  |

### Product Categories

- Furniture
- Office Supplies
- Technology

### Business Regions

- Central
- East
- South
- West

**Dataset Location:**

```text
data/
└── superstore.csv
```

---

## 🔍 Exploratory Data Analysis (EDA)

Exploratory Data Analysis was performed to understand the dataset, identify business patterns, and discover important relationships between sales, discounts, and profit.

### EDA Activities

- Analyzed dataset dimensions and column information.
- Examined numerical statistics using descriptive analysis.
- Checked missing values and duplicate records.
- Identified unique values in categorical columns.
- Analyzed total sales across product categories.
- Compared profit performance across business regions.
- Identified loss-making products.
- Examined the impact of discounts on profit.

### Key EDA Observations

- Technology records the highest total sales among the three product categories.
- The West region records the highest total profit among the four regions.
- Certain products generate high sales but still experience negative profit.
- Discount levels are an important factor to investigate when analyzing loss-making orders.

These observations are based on the supplied Superstore dataset.

---

## 🧹 Data Preparation

The dataset is prepared before training the Machine Learning model.

### Data Preprocessing Steps

1. Loaded the Superstore dataset using Pandas.
2. Removed rows containing missing values using `dropna()`.
3. Selected relevant input features.
4. Separated input variables and target variable.
5. Split the dataset into training and testing subsets.

### Input Features

The model uses the following three features:

- `Sales`
- `Quantity`
- `Discount`

### Target Variable

- `Profit`

**Note:** The supplied model training script does not apply additional feature encoding or scaling.

---

## 🤖 Machine Learning Model

### Linear Regression

The project uses **Linear Regression**, a supervised Machine Learning algorithm, to predict business profit based on sales, quantity, and discount information.

Linear Regression learns the relationship between independent variables and a continuous numerical target variable.

### Model Configuration

| Parameter       | Configuration             |
| --------------- | ------------------------- |
| Algorithm       | Linear Regression         |
| Input Features  | Sales, Quantity, Discount |
| Target Variable | Profit                    |
| Training Data   | 80%                       |
| Testing Data    | 20%                       |
| Random State    | 42                        |
| Library         | Scikit-learn              |

### Model Training Workflow

1. Load the Superstore dataset.
2. Remove rows containing missing values.
3. Select Sales, Quantity, and Discount as input features.
4. Select Profit as the target variable.
5. Split the dataset into training and testing data.
6. Train the Linear Regression model.
7. Save the trained model using Pickle.

### Saved Model Files

**Trained Model:**

```text
models/profit_model.pkl
```

**Model Training Script:**

```text
models/train_model.py
```

**Model Evaluation:**

The current training script does not calculate MAE, MSE, RMSE, or R² scores. Therefore, model performance metrics have not been reported here.

---

## 🧠 Decision Intelligence Logic

The project combines Machine Learning predictions with rule-based business logic to convert predicted profit into understandable business recommendations.

### 1. Profit-Based Recommendations

The predicted profit is compared against predefined thresholds to determine the appropriate business recommendation.

### 2. Business Health Score

The overall business health score is calculated based on the profit margin.

- Profit margins between -20% and +20% are mapped to a score between 0 and 100.
- Values outside this range are capped at the minimum or maximum score.

### 3. Scenario Health Score

The scenario health score adjusts the baseline business health score according to the predicted profit of the selected scenario.

**Important:** Business health scores and recommendations are custom rule-based indicators. They are not separate Machine Learning models or statistically validated business ratings.

---

## 🔄 Project Workflow

The project follows an end-to-end Business Analytics and Machine Learning workflow.

```text
                Superstore Dataset
                        |
                        v
                  Data Loading
                        |
                        v
                Data Understanding
                        |
                        v
          Exploratory Data Analysis
                        |
                        v
             Sales & Profit Analysis
                        |
                        v
       Loss-Making Product Identification
                        |
                        v
                 Feature Selection
                        |
                        v
                 Train-Test Split
                        |
                        v
              Linear Regression Model
                        |
                        v
                  Model Training
                        |
                        v
                 Save Trained Model
                        |
                        v
                 FastAPI Backend
                        |
                        v
       Business Logic & Decision Recommendations
                        |
                        v
              Interactive Dashboard
                        |
                        v
          Profit Prediction & Simulation
```

---

## 🌐 Application Architecture

The main web application follows a **Frontend–Backend Architecture**.

### Frontend Development

**Technologies: HTML, CSS, JavaScript, Chart.js**

The frontend provides an interactive user interface with the following modules:

- Business Overview
- Sales Analytics
- Loss Products
- Profit Simulator
- Business Insights

### Backend Development

**Technologies: Python, FastAPI, Uvicorn**

The backend handles:

- Loading the dataset.
- Loading the trained Machine Learning model.
- Applying category and region filters.
- Calculating business metrics.
- Preparing sales and profit chart data.
- Retrieving loss-making products.
- Generating business insights.
- Performing profit predictions.
- Calculating discount scenario results.

### API Endpoints

The FastAPI backend provides the following endpoints:

| Endpoint                 | Method | Description                                           |
| ------------------------ | ------ | ----------------------------------------------------- |
| `/api/health`            | GET    | Checks API availability                               |
| `/api/filters`           | POST   | Returns available categories and regions              |
| `/api/products`          | POST   | Returns products based on selected filters            |
| `/api/metrics`           | POST   | Returns sales, profit, margin, and health score       |
| `/api/sales_by_category` | POST   | Returns sales grouped by category                     |
| `/api/profit_by_region`  | POST   | Returns profit grouped by region                      |
| `/api/loss_products`     | POST   | Returns loss-making product records                   |
| `/api/insights`          | POST   | Generates business insights                           |
| `/api/simulate_single`   | POST   | Predicts profit for one selected product and discount |
| `/api/simulate_scenario` | POST   | Calculates predictions for multiple product scenarios |

---

## 📁 Project Structure

The project is organized into separate folders for backend development, frontend development, data, Machine Learning models, notebooks, and business logic.

```text
Decision-Intelligence-AI-Business-Dashboard/
│
├── backend/
│   ├── __init__.py
│   ├── main.py
│   ├── utils.py
│   └── requirements.txt
│
├── dashboard/
│   └── app.py
│
├── data/
│   └── superstore.csv
│
├── frontend/
│   ├── index.html
│   ├── sales.html
│   ├── losses.html
│   ├── simulator.html
│   ├── insights.html
│   ├── styles.css
│   └── app.js
│
├── models/
│   ├── profit_model.pkl
│   └── train_model.py
│
├── notebooks/
│   ├── analysis.ipynb
│   └── eda.ipynb
│
├── src/
│   ├── business_logic.py
│   └── insights.py
│
├── requirements.txt
└── README.md
```

---

## ▶️ How to Run the Project

Follow these steps to run the project locally.

### Step 1: Clone the Repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

Navigate to the project directory:

```bash
cd Decision-Intelligence-AI-Business-Dashboard
```

### Step 2: Create a Virtual Environment

```bash
python -m venv .venv
```

### Step 3: Activate the Virtual Environment

**Windows:**

```bash
.venv\Scripts\activate
```

**macOS / Linux:**

```bash
source .venv/bin/activate
```

### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 5: Verify Required Files

Make sure the following files are available:

```text
data/superstore.csv
models/profit_model.pkl
backend/main.py
frontend/index.html
```

### Step 6: Start the Backend Server

Run the following command from the project root directory:

```bash
uvicorn backend.main:app --reload
```

### Step 7: Open the Dashboard

Open your browser and visit:

```text
http://127.0.0.1:8000
```

The FastAPI backend serves the frontend pages and provides the API endpoints used by the dashboard.

### Step 8: Explore API Documentation

FastAPI provides interactive API documentation.

Visit:

```text
http://127.0.0.1:8000/docs
```

---

## 📊 Dashboard Modules

| Module            | Functionality                                             |
| ----------------- | --------------------------------------------------------- |
| Business Overview | Displays key business performance indicators              |
| Sales Analytics   | Visualizes sales by category and profit by region         |
| Loss Products     | Identifies products and orders generating negative profit |
| Profit Simulator  | Predicts profit after changing product discount           |
| Business Insights | Displays automated business observations                  |

---

## ⚠️ Project Limitations

- The Machine Learning model uses only three input features: Sales, Quantity, and Discount.
- Linear Regression may not capture all complex and nonlinear business relationships.
- Predictions are based on historical dataset patterns.
- Recommendations use predefined thresholds and may not cover every business situation.
- The business health score is based on a custom formula.
- The dataset represents historical transactions and may not reflect current market conditions.
- Actual business profit may also depend on operating costs, shipping expenses, seasonality, competition, and other factors not included as model inputs.
- Model evaluation metrics are not currently reported by the supplied training script.

---

## 🚀 Future Enhancements

- Evaluate model performance using MAE, MSE, RMSE, and R².
- Compare Linear Regression with Random Forest, Decision Tree, and other regression algorithms.
- Perform hyperparameter tuning and cross-validation.
- Introduce additional business and product-related features.
- Improve discount and pricing scenario analysis.
- Implement time-based sales and profit forecasting.
- Integrate explainable AI techniques such as SHAP.
- Add downloadable business reports.
- Improve dashboard filtering and visualization capabilities.
- Deploy the application to a cloud platform.

---

## 👩‍💻 Project Information

**Project Name:** Decision Intelligence AI – Business Dashboard

**Project Domain:** Business Analytics and Machine Learning

**Key Concepts:**

- Business Intelligence
- Exploratory Data Analysis
- Machine Learning
- Linear Regression
- Profit Prediction
- Decision Support Systems
- Interactive Data Visualization

**Technologies:** Python | Pandas | NumPy | Scikit-learn | FastAPI | HTML | CSS | JavaScript | Chart.js

---

_This project demonstrates how historical business data, Machine Learning, and rule-based decision intelligence can be combined to analyze business performance, identify potential losses, predict profitability, and support informed business decisions._
