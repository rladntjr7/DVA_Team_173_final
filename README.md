# Stock Market Dashboard

## 📈 Project Overview

This interactive D3.js-based dashboard visualizes popular US stocks listed in the S&P 500. It integrates historical price data with social media sentiments, providing users with insights through sentiment analysis, stock correlation analysis, and performance metrics. 

Our goal is to make financial insights accessible to everyone, especially those without extensive trading experience, through easy-to-interpret visuals and clear descriptions.

This project is available online at [https://gderiddershanghai.github.io/dva_team173_frontend/](https://gderiddershanghai.github.io/dva_team173_frontend/).

![Dashboard Preview](dashboard_preview.png)

## ✨ Features

### 📊 Main Control Section
- **Stock Selection**: Search bar with auto-suggestions for S&P 500 stocks
- **Stock Summary**: Displays stock full name and last price information

### 📉 Main Line Chart
- **Historical Price Trends**: Interactive visualization of stock price history
- **Moving Averages**: Toggle switch for 7, 14, 30, and 90-day moving averages
- **Range Selector**: Interactive slider to select custom date ranges for analysis

### 🔍 Sentiment Analysis
- **Real-time Processing**: Keywords extracted from tweets are processed on-demand
- **Sentiment Visualization**: Interactive bubble chart showing:
  - Keyword sentiment scores
  - Frequency of mentions
  - Relationships between keywords
- **Interactive Elements**: Users can drag bubbles to customize their view

### 🔄 Correlation Chart
- **Stock Correlations**: Displays the most and least correlated stocks to your selection
- **Comparative Analysis**: Selected stock's graph is overlaid for easy comparison

### 📋 Performance Table
- **Key Metrics**: Shows important performance indicators including:
  - Alpha and Beta values
  - Sharpe and Treynor ratios
- **Market Comparison**: Compares metrics against the S&P 500 benchmark
- **Visual Indicators**: Uses charts to show relative performance

## 🛠️ Technology Stack

### Frontend
- **D3.js**: For data visualization components
- **HTML/CSS/JavaScript**: Core web technologies
- **Interactive Elements**: Custom-built sliders, toggles, and draggable components

### Backend
- **FastAPI**: Python-based API server for data processing
- **Pandas/NumPy**: For financial calculations and data manipulation
- **Sentiment Analysis**: Natural language processing for social media data

## 📊 Data Sources

- **Stock Price Data**: 
  - [US Stock Dataset (Kaggle)](https://www.kaggle.com/datasets/footballjoe789/us-stock-dataset)

- **Twitter Data**:
  - [Tweet Sentiment's Impact on Stock Returns](https://www.kaggle.com/datasets/thedevastator/tweet-sentiment-s-impact-on-stock-returns)
  - [IEEE Stock Market Tweets Dataset](https://ieee-dataport.org/open-access/stock-market-tweets-data)
  - [Stock Tweets for Sentiment Analysis](https://www.kaggle.com/datasets/equinxx/stock-tweets-for-sentiment-analysis-and-prediction)
  - [Tweets About Top Companies (2015-2020)](https://www.kaggle.com/datasets/omermetinn/tweets-about-the-top-companies-from-2015-to-2020)

- **Clean Datasets**:
  - [Processed Datasets (Google Drive)](https://drive.google.com/drive/folders/1PPvOJULRUWUcHZwWMKx_v-nUEV7TC_U7?usp=drive_link)

## 🤖 BERT Finetuning & Modeling

The BERT model was used to generate sentiment scores for tweets:

- **Tweet Normalization**: Custom normalization for BERT inputs (`data_processing/TweetNormalizer.py`)
- **Dataset Preparation**: Loading and formatting tweet datasets for training (`data_processing/dataset_loader.py`, `data_processing/notebooks/training_data_set_creation.ipynb`)
- **Model Finetuning**: Custom regression head for sentiment prediction (`data_processing/tweet_bert_finetune.py`, `data_processing/sentiment_trainer.py`)
- **Prediction Pipeline**: System to score new tweets by sentiment (`data_processing/predict_tweets.py`)

## 🧹 Data Processing

### Data Cleaning & Merging
- Duplicate tweet removal (`data_processing/notebooks/ginger/check_for_duplicates.ipynb`)
- Dataset standardization and cleaning (`data_processing/notebooks/cleaning_carinas_labelled_dataset.ipynb`)
- Stock ticker selection based on tweet volume (`data_processing/get_target_stocks.py`)
- Dataset combination from multiple sources (`data_processing/notebooks/merging_all_datasets.ipynb`, `data_processing/notebooks/reducing_the_large_dataset.ipynb`, `data_processing/notebooks/big_tweets.ipynb`)

### Tweet Cleaning & Stopwords
- Custom stopword filtering logic (`data_processing/common_words/filter_stopwords.py`)
- Tweet cleaning functions (`data_processing/common_words/tweet_cleaner.py`)
- Sentiment distribution analysis (`data_processing/notebooks/histograms/`)
- Final tweet consolidation (`data_processing/notebooks/split stocks.ipynb`)

### Keyword Extraction
- Top word extraction algorithms (`calculations/get_common_words.py`)
- Adjacency matrix creation for keyword relationships (`calculations/get_common_words.py`)
- Word form normalization and spelling correction (`calculations/word_mapping.py`)

## 📥 Installation

### Option 1: Run Locally
1. Clone the repository:
   ```bash
   git clone https://github.com/rladntjr7/DVA_Team_173_final.git
   ```
2. Set up a Python virtual environment (Python 3.8+ recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

### Option 2: Use the Live Demo
Visit our hosted version at [https://gderiddershanghai.github.io/dva_team173_frontend/](https://gderiddershanghai.github.io/dva_team173_frontend/)

*Note: The cloud-hosted version may be slower than running locally due to resource limitations.*

## 🚀 Execution

1. Start the backend server:
   ```bash
   python calculations/calculation_api.py
   ```

2. Launch a local server for the frontend:
   - Using VS Code: Install the "Live Server" extension, right-click on `src/index.html` and select "Open with Live Server"
   - Using Python: `python -m http.server` in the project directory
   - Using Node.js: `npx serve` in the project directory

3. Open your browser and navigate to the local server address (typically http://localhost:5500 or http://localhost:8000)

## 🎥 Demo

Watch our demo video: [https://youtu.be/CzXxti6U2Lc](https://youtu.be/CzXxti6U2Lc)

## 👥 Team Members

- Ginger Armando de Ridder
- Jason Othniel Lim
- Wooseok Kim
- Carina Lim
- Gwan-Hyeong Song

---

*Note: This README was formatted with assistance from a generative AI tool.*