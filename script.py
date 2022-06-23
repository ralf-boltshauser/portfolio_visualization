
# Quick demo of yfinance

import math
import matplotlib.pyplot as plt
import yfinance as yf
import datetime
from yahoo_fin.stock_info import get_data
import pandas as pd

start_money = 10000

# start date today - 10 years
start_date = (datetime.datetime.now() -
              datetime.timedelta(days=3*365)).strftime("%Y-%m-%d")
end_date = datetime.datetime.now().strftime("%Y-%m-%d")
print(start_date)
print(end_date)

portfolios = [
    {
        "name": "70/30",
        "tickers": [{
            "code": "URTH",
            "weight": 0.7,
            "data": None,
            "shares_amount": 0,
        }, {
            "code": "EMRD.L",
            "weight": 0.3,
            "data": None,
            "shares_amount": 0,
        }],
        "total_value": None,
    },
    {
        "name": "VT/CHSPI",
        "tickers": [{
            "code": "VT",
            "weight": 0.8,
            "data": None,
            "shares_amount": 0,
        }, {
            "code": "CHSPI.SW",
            "weight": 0.2,
            "data": None,
            "shares_amount": 0,
        }],
        "total_value": None,
    },
]


# Plot layout
fig, axs = plt.subplots(2, 1, figsize=(10, 10))
fig.suptitle("Portfolio Performance", fontsize=20)
individual_tickers_plot = axs[0]
portfolio_returns_plot = axs[1]

individual_tickers_plot.set_title("Individual Tickers")
portfolio_returns_plot.set_title("Portfolio Returns")


ticker_list = []

for portfolio in portfolios:
    for ticker in portfolio["tickers"]:
        ticker_list.append(ticker["code"])

data = yf.download(ticker_list, start_date, end_date)['Adj Close']

# Plot all the close prices
individual_tickers_plot.plot(
    data.index, (data.pct_change()+1).cumprod().values)
print(data.head())
# Show the legend
individual_tickers_plot.legend(data.columns)

# Define the label for the title of the figure

# Define the labels for x-axis and y-axis
individual_tickers_plot.set_ylabel('Cumulative Returns', fontsize=14)

# Plot the grid lines
individual_tickers_plot.grid(
    which="major", color='k', linestyle='-.', linewidth=0.5)
# Calculate portfolio values for each day
for portfolio in portfolios:

    for ticker in portfolio["tickers"]:
        ticker["data"] = data[ticker["code"]]
        first_value = ticker["data"].loc[ticker['data'].first_valid_index()]
        ticker["shares_amount"] = math.floor(
            start_money * ticker["weight"] / first_value)
        # print(ticker["code"])
        # print("Shares amount", ticker["shares_amount"])
        # print("First Value", first_value)
        # print("Last Value", data[ticker["code"]].iloc[-1])
        # calculate value for each day
        data[ticker["code"]] = (data[ticker["code"]] *
                                ticker["shares_amount"])
        # get the last value
        ticker["data"] = data[ticker["code"]]
        # print("Last Value Multiplied", data[ticker["code"]].iloc[-1])
        if portfolio["total_value"] is None:
            portfolio["total_value"] = data[ticker["code"]]
        else:
            portfolio["total_value"] += data[ticker["code"]]


# Plot all the close prices
portfolios_data = {}
for portfolio in portfolios:
    portfolios_data[portfolio["name"]] = portfolio["total_value"]
portfolios_dataframe = pd.DataFrame(portfolios_data)
print(portfolios_dataframe.head())

portfolio_returns_plot.plot(
    portfolios_dataframe.index, portfolios_dataframe.values)

# Show the legend
portfolio_returns_plot.legend(portfolios_dataframe.columns)

# Define the label for the title of the figure

# Define the labels for x-axis and y-axis
portfolio_returns_plot.set_ylabel('Cumulative Returns', fontsize=14)
portfolio_returns_plot.set_xlabel('Year', fontsize=14)

# Plot the grid lines
portfolio_returns_plot.grid(
    which="major", color='k', linestyle='-.', linewidth=0.5)

plt.show()
