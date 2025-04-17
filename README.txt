DVA_Team_173 - Stock Market Dashboard

Description

Project overview
This project is an interactive D3.js based dashboard for popular US stocks listed in S&P 500. It integrates historical price data with social media sentiments, providing users with insights through sentiment analysis, stock correlation analysis, and performance metrics. Our goal was to provide financial insights to everyone, especially to those who does not have extensive trading history, by easy-to-interpret visuals and clear descriptions. This project is mainly based on Javascript and Python, where the frontend portion is controlled by Javascript codes, and the backend data pulling and processing is done by Python code, with using FastAPI as the connection.

Visualization
With the aid of D3.js, we successfully produced the following features in our dashboard.
- Main control section: Users can select the stock by searchbar and get summary, such as stock full name and last price.
- Main linechart: Linechart shows historical price trends, with toggle switch available to enable/disable moving average lines in various options. A slider with two button is placed at the bottom of the chart, on which the users can slide and set the range that they want to see analysis on. Whenever a user selects the range, the whole dashboard updates with the new range selected.
- Sentiment chart: Keywords extracted from millions of tweets are being process real-time when user selects stock and the range, showing the keywords' sentiment scores, frequencies, and the relationships between them. The user can move around the "bubbles" in whichever way they want, changing the chart in any way that allows better insight extraction.
- Correlation chart: The most and least correlated stock to the selected stock is shown in a form of linechart. Selected stock's graph is overlayed for the users easily track the difference or similarity to the stocks presented.
- Performance table: This table shows the most relevant performance metrics of the selected stock. The calculation is done in real-time and shows the comparison between the market average (S&P 500) in a form of linear chart. 

Data Cleaning
*Ginger's part*

Backend
Our visualization constantly sends and receives information from our backend, a Python based FastAPI server. Whenever a user's input is processed, either selecting a new stock or dragging the sliders to set a date range, our JS code sends a request to the server. When a request is received, the API sends back the stock price data, perforamnce metrics, and sentiment analysis results to be used by the Frontend to update the dashboard. This way, hosting the websites on platforms such as GitHub Pages has become a lot easier since it does not require for the JS code to load the data locally. 

Installation
To install our code is very straightforward and simple - just clone our repository on the GitHub link "LINK TO BE ADDED HERE". After cloning (or directly downloading from the repository), set a virtual environment with latest Python version with your favorite setup methods (venv, conda, etc.) and download packages listed in requirements.txt file. 
There is another way that does not require any download/installation - our page hosted on GitHub Pages! We already hosted all our codes to GitHub and Cloud. The page is accessible with the link "https://gderiddershanghai.github.io/dva_team173_frontend/". Please note that the performance on the cloud is significantly slower than running on local devices, due to compromises made in resource selection on cloud.

Execution
If you chose to run locally, you can follow the following steps:
1. On your IDE (we recommend VSCode), change your directory in both the explorer and the terminal.
2. Activate the virtual enviroment where the required Python packages are installed.
3. Run calculation_api.py to activate the FastAPI server.
4. Launch a local server to open the webpage. There are plenty of options available, but we recommend using "Live Server" extension on VSCode. Just right-click on the index.html file inside the IDE's explorer and select "Open with Live Server".
5. You can now enjoy the dashboard with plenty of visualization and helpful insights!