# KuCoinPriceRetrieval

Welcome to a high-performance Python script leveraging KuCoin's API for cryptocurrency price retrieval. Utilizes multithreading to overcome API request limitations, enabling seamless data storage in Excel for comprehensive time-series analysis.

You can control the interval using timestamp (there are functions to control the desired timestamp easily) and with the a lot of temporalities (1min, 5min, 15min, 1hour, 4hour, 8hour, 1day, 1week, 1month).

I'm testing an AI to do models for prices predictions using LSTM neuronal networks. You can access to an alpha.

Functions:
- (Market Data) Work with timestamps.
- (Market Data) Retrieve prices for a lot of cryptocurrencies.
- (Market Data)Retrieve prices using multithreading.
- (Market Data) Write data of prices on Excel.
- (Graph) Plot price data.
- (Trading) Introducing your KuCoin's credentials, you can put limit orders and cancel them.
- (LSTM_Train) Train an AI model.
- (LSTM_Train) Test an AI model. 
