# this file calculates the performance, correlation, and sentiment of a stock with a given date range
# it uses the stock data, twit data and use FastAPI to interact with the javascript frontend
# the frontend will send the stock ticker, start date, and end date
# the backend will calculate the performance, correlation, and sentiment of the stock

# the frontend will send the following data:
# {
#     "stock_ticker": xx,
#     "start_date": xx,
#     "end_date": xx,
# }

# the backend will return the results to the frontend with the following format:
# {
#     "performance": {
#         "alpha": xx,
#         "alpha_rank": xx,
#         "market_alpha": xx,
#         "beta": xx,
#         "beta_rank": xx,
#         "market_beta": xx,
#         "sharpe_ratio": xx,
#         "sharpe_ratio_rank": xx,
#         "market_sharpe_ratio": xx,
#         "treynor_ratio": xx,
#         "treynor_ratio_rank": xx,
#         "market_treynor_ratio": xx,
#     },
#     "correlation": {
#         "most_correlated_stock": xx,
#         "most_correlated_stock_correlation": xx,
#         "least_correlated_stock": xx,
#         "least_correlated_stock_correlation": xx,
#     },
#     "sentiment": {
#         "keywords" : {
#             "keyword1": {
#                 "sentiment_score": xx,
#                 "count": xx,
#                 "keyword2": xx, number of times keyword 1 appears with keyword 2 in the tweets
#                 "keyword3": xx, number of times keyword 1 appears with keyword 3 in the tweets
#                 ...
#             },
#             "keyword2": {
#                 "sentiment_score": xx,    
#                 "count": xx,
#                 "keyword1": xx, number of times keyword 2 appears with keyword 1 in the tweets
#                 "keyword3": xx, number of times keyword 2 appears with keyword 3 in the tweets
#                 ...
#             },
#             ...
#         }
#     }
# }


# Dir of the tweet data - @Kenny, might have to change this
TWEET_DATA_DIR = "clean_data/twit_data/non_neutral" # non neutral is neutral tweets are filtered out

# stock data is saved in the following path with individual csv files for each stock with the ticker as the name
# the csv file contains the following columns:
# Date, Open, High, Low, Close, Volume
STOCK_DATA_PATH = "clean_data/stock_data"

STOCK_TICKERS = ["CSCO", "BA", "V", "T", "BAC", "F", "PEP", "COST", "MRK", "ORCL", "SBUX", "PG", "MCD", "AMZN", "INTC", "KO", "PYPL", "UPS", "MSFT", "AMD", "HD", "XOM", "CVX", "CMCSA", "NKE", "KR", "IBM", "DIS", "NFLX", "JPM", "TSLA", "SPY", "GOOGL", "META", "PFE", "UNH", "MA", "AAPL", "WMT", "JNJ"]

# the performance metrics will be calculated with using SPY as the benchmark
# when a data is received, all metrics will be calculated for all the stocks in the STOCK_TICKERS list and get the rank accoring to the results
# risk_free_rate is 0.02 per year
RISK_FREE_RATE = 0.02

# the sentiment analysis will be done by repeating the following steps:
# 1. get the tweets for the given stock and date range
# 2. make a dictionary of the keywords that appear in the tweets
# 3. for each tweet and its sentiment score, add the sentiment score to the dictionary for each keyword from the given tweet to the previous sentiment score
# 4. export the dictionary to the given format for the top 10 keywords by count

import os
import pandas as pd
import numpy as np
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from datetime import datetime
import re
from fastapi.middleware.cors import CORSMiddleware
from collections import defaultdict
from get_common_words import CommonWords


app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class StockRequest(BaseModel):
    stock_ticker: str
    start_date: str
    end_date: str
    
class WordBubbleRequest(BaseModel):
    ticker: str
    start_date: str
    end_date: str
    min_count_percentage: Optional[float] = 0.015
    top_n_words: Optional[int] = 7
    filter_metric: Optional[str] = "average_score"
    

def load_stock_data(ticker: str, start_date: str, end_date: str) -> pd.DataFrame:
    file_path = os.path.join(STOCK_DATA_PATH, f"{ticker}.csv")
    try:
        df = pd.read_csv(file_path)
        df['Date'] = pd.to_datetime(df['Date'], utc=True)
        # Convert string dates to datetime
        start_date_dt = pd.to_datetime(start_date, utc=True)
        end_date_dt = pd.to_datetime(end_date, utc=True)
        # Filter by date range
        df = df[(df['Date'] >= start_date_dt) & (df['Date'] <= end_date_dt)]
        return df
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail=f"Stock data for {ticker} not found")

def calculate_returns(stock_data: pd.DataFrame) -> float:
    # Calculate total return over the period
    first_price = stock_data['Close'].iloc[0]
    last_price = stock_data['Close'].iloc[-1]
    total_return = (last_price / first_price) - 1
    return total_return

def calculate_performance_metrics(stock_return: float, market_return: float, stock_data: pd.DataFrame, market_data: pd.DataFrame) -> dict:
    # Convert annual risk-free rate to the period return
    # Assuming 252 trading days in a year
    
    # Calculate period length in trading days
    period_days = len(stock_data)
    if period_days < 1:
        period_days = 1  # Default to 1 if no data available
    
    # Calculate the period's risk-free rate
    period_risk_free_rate = RISK_FREE_RATE * (period_days / 252)
    
    # Calculate excess returns for the period
    excess_stock_return = stock_return - period_risk_free_rate
    excess_market_return = market_return - period_risk_free_rate
    
    # Since we have daily data, we can calculate beta properly using the daily returns
    # Calculate daily returns for beta calculation
    daily_stock_returns = stock_data['Close'].pct_change().dropna().values
    daily_market_returns = market_data['Close'].pct_change().dropna().values
    
    # Ensure arrays are the same length
    min_length = min(len(daily_stock_returns), len(daily_market_returns))
    if min_length > 1:
        beta = np.cov(daily_stock_returns[:min_length], daily_market_returns[:min_length])[0, 1] / np.var(daily_market_returns[:min_length])
    else:
        beta = 1.0  # Default value
    
    # Alpha: stock return - (risk-free rate + beta * (market return - risk-free rate))
    alpha = stock_return - (period_risk_free_rate + beta * (market_return - period_risk_free_rate))
    
    # Calculate Sharpe ratio using the period return and annualized volatility
    # For more accurate Sharpe, we use daily returns to estimate volatility
    if min_length > 1:
        # Annualize the volatility
        daily_volatility = np.std(daily_stock_returns)
        annualized_volatility = daily_volatility * np.sqrt(252)
        sharpe_ratio = excess_stock_return / annualized_volatility if annualized_volatility != 0 else 0
    else:
        sharpe_ratio = excess_stock_return / period_risk_free_rate if period_risk_free_rate != 0 else 0
    
    # Calculate Treynor ratio
    treynor_ratio = excess_stock_return / beta if beta != 0 else 0
    
    return {
        "alpha": float(alpha),
        "beta": float(beta),
        "sharpe_ratio": float(sharpe_ratio),
        "treynor_ratio": float(treynor_ratio)
    }

def calculate_correlation(request_ticker: str, stock_data: pd.DataFrame, all_stocks_data: Dict[str, pd.DataFrame]) -> dict:
    """Calculate true Pearson correlation between stocks using daily returns."""
    if not stock_data.empty and len(all_stocks_data) > 0:
        # Calculate daily returns for the requested stock
        stock_returns = stock_data['Close'].pct_change().dropna()
        
        # Calculate correlations with all other stocks
        correlations = {}
        for ticker, data in all_stocks_data.items():
            # Skip the requested stock itself and SPY (benchmark)
            if ticker == request_ticker or ticker == "SPY" or data.empty:
                continue
                
            # Calculate daily returns for comparison stock
            compare_returns = data['Close'].pct_change().dropna()
            
            # Align the two return series to ensure they have matching dates
            aligned_returns = pd.concat([stock_returns, compare_returns], axis=1, join='inner')
            aligned_returns.columns = ['stock', 'compare']
            
            # Skip if not enough data points for correlation
            if len(aligned_returns) < 5:
                continue
                
            # Calculate Pearson correlation
            corr = aligned_returns['stock'].corr(aligned_returns['compare'])
            if not np.isnan(corr):
                correlations[ticker] = corr
        
        if not correlations:
            return {
                "most_correlated_stock": "None",
                "most_correlated_stock_correlation": 0,
                "least_correlated_stock": "None",
                "least_correlated_stock_correlation": 0
            }
        
        # Find most and least correlated stocks
        most_correlated = max(correlations.items(), key=lambda x: x[1])
        least_correlated = min(correlations.items(), key=lambda x: x[1])
        
        return {
            "most_correlated_stock": most_correlated[0],
            "most_correlated_stock_correlation": float(most_correlated[1]),
            "least_correlated_stock": least_correlated[0],
            "least_correlated_stock_correlation": float(least_correlated[1])
        }
    
    return {
        "most_correlated_stock": "None",
        "most_correlated_stock_correlation": 0,
        "least_correlated_stock": "None",
        "least_correlated_stock_correlation": 0
    }

# def extract_keywords(tweet: str) -> List[str]:
#     # Tweet column already contains cleaned keywords separated by spaces
#     # Ensure the tweet is a string before splitting
#     if not isinstance(tweet, str):
#         tweet = str(tweet)
#     return tweet.split()

# def analyze_sentiment(twitter_data: pd.DataFrame) -> dict:
#     if twitter_data.empty:
#         return {"keywords": {}}
    
#     # Initialize data structures
#     keyword_data = defaultdict(lambda: {"sentiment_score": 0, "count": 0})  # Track sentiment and count for each keyword
#     keyword_tweets = defaultdict(set)  # Using sets instead of lists for faster intersection operations
    
#     # First pass: Process each tweet to extract keywords and track their tweets
#     for idx, row in twitter_data.iterrows():
#         tweet = row['Tweet']
#         score = row['Score']
        
#         # Extract keywords
#         keywords = extract_keywords(tweet)
        
#         # Update keyword data and track which tweet index the keyword appears in
#         for keyword in keywords:
#             keyword_data[keyword]["sentiment_score"] += score
#             keyword_data[keyword]["count"] += 1
#             keyword_tweets[keyword].add(idx)
    
#     # Sort keywords by count and take top 8
#     top_keywords = sorted(keyword_data.items(), key=lambda x: x[1]["count"], reverse=True)[:8]
#     top_keyword_names = [k for k, _ in top_keywords]
    
#     # Prepare final format with precalculated average sentiment
#     result = {"keywords": {}}
    
#     # Calculate average sentiment and add base data for each top keyword
#     for keyword, data in top_keywords:
#         avg_sentiment = data["sentiment_score"] / data["count"] if data["count"] > 0 else 0
#         result["keywords"][keyword] = {
#             "sentiment_score": float(avg_sentiment),
#             "count": data["count"]
#         }
    
#     # Precompute co-occurrences matrix for top keywords only - much more efficient
#     # Create a dictionary to store precomputed intersections
#     co_occurrences = {}
    
#     # For each pair of top keywords, calculate intersection once
#     for i, keyword1 in enumerate(top_keyword_names):
#         for keyword2 in top_keyword_names[i+1:]:  # Only compute each pair once
#             # Find intersection of tweet indices
#             common_count = len(keyword_tweets[keyword1] & keyword_tweets[keyword2])
#             if common_count > 0:
#                 co_occurrences[(keyword1, keyword2)] = common_count
#                 co_occurrences[(keyword2, keyword1)] = common_count  # Store both directions
    
#     # Add co-occurrence data to result
#     for keyword in top_keyword_names:
#         for other_keyword in top_keyword_names:
#             if keyword != other_keyword:
#                 count = co_occurrences.get((keyword, other_keyword), 0)
#                 if count > 0:
#                     result["keywords"][keyword][other_keyword] = count
    
#     return result

@app.post("/api/word-bubbles")
async def word_bubbles_endpoint(req: WordBubbleRequest):
    print('TRYING TO GET SENTIMENT DATAAAAA')
    try:
        print('what does a man gotta ado to get some sentiment data around here')
        analyzer = CommonWords(
            ticker=req.ticker.upper(),
            data_dir=TWEET_DATA_DIR,
            start_date=req.start_date,
            end_date=req.end_date,
            min_count_percentage=req.min_count_percentage,
            top_n_words=req.top_n_words,
            filter_metric=req.filter_metric,
        )

        result = analyzer.calculate()

        if result is None:
            raise HTTPException(status_code=404, detail="No data found for this query.")

        top_words, bottom_words, adj_matrix = result
        # print('WRONG FUCKING WORDS', top_words,  bottom_words)
        # print("TYPE OF top_words[0]:", type(top_words[0]))

        return {
            "top_words": top_words,
            "bottom_words": bottom_words,
            "adj_matrix": adj_matrix,
        }

    except FileNotFoundError as e:
        # print('404 could not get that data')
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        # print('oopsies internal error')
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")


@app.post("/api/stock_data")
async def stock_data(request: StockRequest):
    try:
        stock_df = load_stock_data(request.stock_ticker, request.start_date, request.end_date)
        # Convert DataFrame to list of dictionaries (records format) for JSON serialization
        stock_data_list = stock_df.to_dict(orient='records')
        return stock_data_list
    except Exception as e:
        import traceback
        traceback.print_exc() # Print full traceback for debugging
        raise HTTPException(status_code=500, detail=f"Error processing stock data: {str(e)}")

@app.post("/api/calculate")
async def calculate(request: StockRequest):
    try:
        # Load data
        stock_data = load_stock_data(request.stock_ticker, request.start_date, request.end_date)
        market_data = load_stock_data("SPY", request.start_date, request.end_date)
        
        # Calculate total returns over the period
        stock_return = calculate_returns(stock_data)
        market_return = calculate_returns(market_data)
        
        # Calculate performance metrics for the requested stock
        performance_metrics = calculate_performance_metrics(stock_return, market_return, stock_data, market_data)
        
        # Calculate performance metrics for all stocks to determine ranks
        all_metrics = {}
        all_returns = {}
        all_stocks_data = {}
        
        for ticker in STOCK_TICKERS:
            # Skip the requested stock - we already calculated its metrics
            if ticker == request.stock_ticker:
                continue
                
            try:
                ticker_data = load_stock_data(ticker, request.start_date, request.end_date)
                ticker_return = calculate_returns(ticker_data)
                all_returns[ticker] = ticker_return
                all_stocks_data[ticker] = ticker_data
                
                metrics = calculate_performance_metrics(ticker_return, market_return, ticker_data, market_data)
                all_metrics[ticker] = metrics
            except Exception:
                # Skip stocks with missing data
                continue
        
        # Calculate ranks
        # Include the requested stock in the metrics for ranking
        combined_metrics = all_metrics.copy()
        combined_metrics[request.stock_ticker] = performance_metrics
        
        alphas = {ticker: metrics["alpha"] for ticker, metrics in combined_metrics.items()}
        betas = {ticker: metrics["beta"] for ticker, metrics in combined_metrics.items()}
        sharpe_ratios = {ticker: metrics["sharpe_ratio"] for ticker, metrics in combined_metrics.items()}
        treynor_ratios = {ticker: metrics["treynor_ratio"] for ticker, metrics in combined_metrics.items()}
        market_alpha = 0
        market_beta = 1
        market_sharpe_ratio = combined_metrics.get("SPY", {"sharpe_ratio": 0})["sharpe_ratio"]
        market_treynor_ratio = combined_metrics.get("SPY", {"treynor_ratio": 0})["treynor_ratio"]

        alpha_rank = sorted(alphas.keys(), key=lambda x: alphas[x], reverse=True).index(request.stock_ticker) + 1 if request.stock_ticker in alphas else 0
        beta_rank = sorted(betas.keys(), key=lambda x: betas[x], reverse=True).index(request.stock_ticker) + 1 if request.stock_ticker in betas else 0
        sharpe_rank = sorted(sharpe_ratios.keys(), key=lambda x: sharpe_ratios[x], reverse=True).index(request.stock_ticker) + 1 if request.stock_ticker in sharpe_ratios else 0
        treynor_rank = sorted(treynor_ratios.keys(), key=lambda x: treynor_ratios[x], reverse=True).index(request.stock_ticker) + 1 if request.stock_ticker in treynor_ratios else 0
        
        # Calculate correlation using time series data, not just total returns
        all_stocks_data[request.stock_ticker] = stock_data
        correlation_data = calculate_correlation(request.stock_ticker, stock_data, all_stocks_data)
        
        # Format response
        response = {
            "performance": {
                "alpha": performance_metrics["alpha"],
                "alpha_rank": alpha_rank,
                "market_alpha": market_alpha,
                "beta": performance_metrics["beta"],
                "beta_rank": beta_rank,
                "market_beta": market_beta,
                "sharpe_ratio": performance_metrics["sharpe_ratio"],
                "sharpe_ratio_rank": sharpe_rank,
                "market_sharpe_ratio": market_sharpe_ratio,
                "treynor_ratio": performance_metrics["treynor_ratio"],
                "treynor_ratio_rank": treynor_rank,
                "market_treynor_ratio": market_treynor_ratio
            },
            "correlation": correlation_data
        }
        
        return response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)