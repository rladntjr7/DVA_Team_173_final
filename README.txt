=====================================
DVA_Team_173 - Stock Market Dashboard
=====================================
- Ginger Armando de Ridder
- Jason Othniel Lim
- Wooseok Kim
- Carina Lim
- Gwan-Hyeong Song

=====================================
Project overview
=====================================
This project is an interactive D3.js based dashboard for popular US stocks listed in S&P 500. It integrates historical price data with social media sentiments, providing users with insights through sentiment analysis, stock correlation analysis, and performance metrics. Our goal was to provide financial insights to everyone, especially to those who does not have extensive trading history, by easy-to-interpret visuals and clear descriptions. This project is mainly based on Javascript and Python, where the frontend portion is controlled by Javascript codes, and the backend data pulling and processing is done by Python code, with using FastAPI as the connection.

=====================================
Visualization
=====================================
With the aid of D3.js, we successfully produced the following features in our dashboard.
- Main control section: Users can select the stock by searchbar and get summary, such as stock full name and last price.
- Main linechart: Linechart shows historical price trends, with toggle switch available to enable/disable moving average lines in various options. A slider with two button is placed at the bottom of the chart, on which the users can slide and set the range that they want to see analysis on. Whenever a user selects the range, the whole dashboard updates with the new range selected.
- Sentiment chart: Keywords extracted from millions of tweets are being process real-time when user selects stock and the range, showing the keywords' sentiment scores, frequencies, and the relationships between them. The user can move around the "bubbles" in whichever way they want, changing the chart in any way that allows better insight extraction.
- Correlation chart: The most and least correlated stock to the selected stock is shown in a form of linechart. Selected stock's graph is overlayed for the users easily track the difference or similarity to the stocks presented.
- Performance table: This table shows the most relevant performance metrics of the selected stock. The calculation is done in real-time and shows the comparison between the market average (S&P 500) in a form of linear chart. 

=====================================
Data Sources
=====================================
STOCK DATA
https://www.kaggle.com/datasets/footballjoe789/us-stock-dataset

TWITTER DATA
Carina Found https://www.kaggle.com/datasets/thedevastator/tweet-sentiment-s-impact-on-stock-returns
IEEE Dataset https://ieee-dataport.org/open-access/stock-market-tweets-data
Kenny https://www.kaggle.com/datasets/equinxx/stock-tweets-for-sentiment-analysis-and-prediction
Large Dataset Ginger https://www.kaggle.com/datasets/omermetinn/tweets-about-the-top-companies-from-2015-to-2020

LINKS TO CLEAN DATASETS (after processing)
https://drive.google.com/drive/folders/1PPvOJULRUWUcHZwWMKx_v-nUEV7TC_U7?usp=drive_link

=====================================
BERT FINETUNING & MODELING
=====================================
BERT model has been used to get sentiment scores for each tweet for our further analysis. Below is a list of files that was used to complete this task.
1. data_processing/TweetNormalizer.py : Custom tweet normalization for BERT inputs as per finetuned model instructions
2. data_processing/dataset_loader.py : Loads and formats tweet datasets for training
3. data_processing/notebooks/training_data_set_creation.ipynb : Generates train/test datasets
4. data_processing/tweet_bert_finetune.py : Loads BERT model + regression head for sentiment prediction
5. data_processing/sentiment_trainer.py : Code for finetuning 
6. data_processing/predict_tweets.py : Code to get score predictions 

=====================================
DATA CLEANING & MERGING
=====================================
Having different datasets with different formats, we needed to find way to make them into a single dataset for further processing.
1. data_processing/notebooks/ginger/check_for_duplicates.ipynb : Removes duplicate tweets
2. data_processing/notebooks/cleaning_carinas_labelled_dataset.ipynb : Cleans Carina’s dataset
3. data_processing/notebooks/reducing_the_large_dataset.ipynb, notebooks/big_tweets.ipynb : Filters and trims large tweet datasets
4. data_processing/notebooks/merging_all_datasets.ipynb : Combines all datasets (Carina, Kenny, Jason, Ginger)
5. data_processing/get_target_stocks.py : Selects target stock tickers based on total number of tweets

=====================================
TWEET CLEANING & STOPWORDS
=====================================
Tweets contains a lot of stopwords in nature, and filtering them was a very important process to get the most relevant keywords from sentiment analysis.
1. data_processing/common_words/filter_stopwords.py : Most of the logix for the tweet_cleaner function
2. data_processing/common_words/tweet_cleaner.py : Function for cleaning the tweets
3. data_processing/notebooks/histograms/ : Score distribution plots to filter neutral sentiment
4. data_processing/notebooks/split stocks.ipynb : Final tweet cleanup & consolidation

=====================================
ADJACENCY MATRIX & TOP WORDS
=====================================
To display keywords in the dashboard, following files filter the top keywords.
1. calculations/get_common_words.py : Extracts the top words & builds adjacency matrix
2. calculations/word_mapping.py : Dictionary to correct spelling and normalize word forms

=====================================
Backend
=====================================
Our visualization constantly sends and receives information from our backend, a Python based FastAPI server. Whenever a user's input is processed, either selecting a new stock or dragging the sliders to set a date range, our JS code sends a request to the server. When a request is received, the API sends back the stock price data, perforamnce metrics, and sentiment analysis results to be used by the Frontend to update the dashboard. This way, hosting the websites on platforms such as GitHub Pages has become a lot easier since it does not require for the JS code to load the data locally. 

=====================================
Installation
=====================================
To install our code is very straightforward and simple - just clone our repository on the GitHub link "https://github.com/rladntjr7/DVA_Team_173_final.git". After cloning (or directly downloading from the repository), set a virtual environment with latest Python version with your favorite setup methods (venv, conda, etc.) and download packages listed in requirements.txt file.
If you wish not to download/clone from our repository, you can still work with what we have in the submitted .zip file. Just head to this Google Drive link "https://drive.google.com/drive/folders/16neNsIPCrI6R0i1HANJnhdv7LXl8XRw3?usp=share_link" and download our dataset. Make sure the "clean_data" folder is located at the root directory of the project folder, on the same level with "calculations" folder.
There is another way that does not require any download/installation - our page hosted on GitHub Pages! We already hosted all our codes to GitHub and Cloud. The page is accessible with the link "https://gderiddershanghai.github.io/dva_team173_frontend/". Please note that the performance on the cloud is significantly slower than running on local devices, due to compromises made in resource selection on cloud.

=====================================
Execution
=====================================
If you chose to run locally, you can follow the following steps:
1. On your IDE (we recommend VSCode), open the folder of the downloaded/cloned project.
2. Activate the virtual enviroment where the required Python packages are installed.
3. Run calculations/calculation_api.py to activate the FastAPI server.
4. Launch a local server to open the webpage. There are plenty of options available, but we recommend using "Live Server" extension on VSCode. Just right-click on the src/index.html file inside the IDE's explorer and select "Open with Live Server".
5. You can now enjoy the dashboard with plenty of visualization and helpful insights! Please play around all our features we provided, including searching for stocks, sliding the date range, playing with the bubbles, etc. Hope you enjoy!