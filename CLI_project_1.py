# Importing relevant libraries, including the one for cryptocurrency API, Coinbase Pro.
import questionary
from MCForecastTools import MCSimulation
import os
import requests
from datetime import date
import pandas as pd
import numpy as np
import cbpro
# Using the public client of Coinbase to collect data
c = cbpro.PublicClient()
# Getting historical data of Bitcoin price and putting it into data frame format in Pandas
Bitcoin = pd.DataFrame(c.get_product_historic_rates('BTC-USD', start = '2021-01-01T01:00:00', end = date.today() , granularity = 86400))
Bitcoin.columns= ["Date","Open","High","Low","Close","Volume"]
Bitcoin['Date'] = pd.to_datetime(Bitcoin['Date'], unit='s')
Bitcoin.set_index('Date', inplace=True)
Bitcoin.sort_values(by='Date', ascending=True, inplace=True)
# Getting historical data of Uniswap price and putting it into data frame format in Pandas
Uniswap= pd.DataFrame(c.get_product_historic_rates('UNI-USD', start = '2021-01-01T01:00:00', end = date.today() , granularity = 86400))
Uniswap.columns= ["Date","Open","High","Low","Close","Volume"]
Uniswap['Date'] = pd.to_datetime(Uniswap['Date'], unit='s')
Uniswap.set_index('Date', inplace=True)
Uniswap.sort_values(by='Date', ascending=True, inplace=True)
# Getting historical data of Steller price and putting it into data frame format in Pandas
Steller=  pd.DataFrame(c.get_product_historic_rates('XLM-USD', start = '2021-01-01T01:00:00', end = date.today() , granularity = 86400))
Steller.columns= ["Date","Open","High","Low","Close","Volume"]
Steller['Date'] = pd.to_datetime(Steller['Date'], unit='s')
Steller.set_index('Date', inplace=True)
Steller.sort_values(by='Date', ascending=True, inplace=True)
# Getting historical data of Ethereum price and putting it into data frame format in Pandas
Ethereum= pd.DataFrame(c.get_product_historic_rates('ETH-USD', start = '2021-01-01T01:00:00', end = date.today() , granularity = 86400))
Ethereum.columns= ["Date","Open","High","Low","Close","Volume"]
Ethereum['Date'] = pd.to_datetime(Ethereum['Date'], unit='s')
Ethereum.set_index('Date', inplace=True)
Ethereum.sort_values(by='Date', ascending=True, inplace=True)
# Getting historical data of Litecoin price and putting it into data frame format in Pandas
Litecoin= pd.DataFrame(c.get_product_historic_rates('LTC-USD', start = '2021-01-01T01:00:00', end = date.today() , granularity = 86400))
Litecoin.columns= ["Date","Open","High","Low","Close","Volume"]
Litecoin['Date'] = pd.to_datetime(Litecoin['Date'], unit='s')
Litecoin.set_index('Date', inplace=True)
Litecoin.sort_values(by='Date', ascending=True, inplace=True)
#Concatinating five cryptocurrencies into one dataframe to start doing analysis on them.
Five_Crypto= pd.concat([Bitcoin, Uniswap, Steller, Ethereum, Litecoin ], axis=1, keys= ["Bitcoin", "Uniswap", "Steller", "Ethereum", "Litecoin"])
# Slicing the closing price out of each dataframe
BTC=Bitcoin.loc[:,'Close']
UNI=Uniswap.loc[:,'Close']
XLM= Steller.loc[:,'Close']
ETH=Ethereum.loc[:,'Close']
LTC= Litecoin.loc[:,'Close']
#Adding all the closing prices to make one dataframe with five columns of closing prices and then titling each column with the relevant coin name.
Five_Crypto_ClosingPrice=pd.concat([BTC,UNI,XLM,ETH,LTC],axis=1)
Five_Crypto_ClosingPrice.columns=['BTC','UNI','XLM','ETH','LTC']
# finding the percentage of change in the closing price for each coin.
Five_Crypto_daily_returns= Five_Crypto_ClosingPrice.pct_change().dropna()
# Finding cumulative return of the price on each coin
Five_Crypto_cumulative_returns=(1+Five_Crypto_daily_returns).cumprod()
User_info_Cumulative_return=Five_Crypto_cumulative_returns.tail(1)
#getting the percentage of change in each coin and showing them to the user.
All_Cumulative_return=User_info_Cumulative_return.values[0]*100
print(f"Here is the cumulative return of five popular cryptocurrencies from the beginning of 2021 \n - Bitcoin: {All_Cumulative_return[0]:.1f}%." 
     f"\n- Uniswap: {All_Cumulative_return[1]:.1f}%."
     f"\n-Steller:{All_Cumulative_return[2]:.1f}%." 
     f"\n-Ethereum: {All_Cumulative_return[3]:.1f}%."
     f" \n-Litecoin: {All_Cumulative_return[4]:.1f}%."
     f"\n The higher the percentage of the cumulative return, the higher the investment profit")

trading_days=Five_Crypto_daily_returns.count()[1]+1
Five_crypto_Annual_average_return=Five_Crypto_daily_returns.mean()*trading_days
Five_Crypto_Annual_std=Five_Crypto_daily_returns.std()* np.sqrt(trading_days)
Five_crypto_Sharpe_ratios=Five_crypto_Annual_average_return/Five_Crypto_Annual_std
print("......................")
print(f"Here is the Sharpe ration of the above five popular cryptocurrencies \n-Bitcoin: {Five_crypto_Sharpe_ratios[0]:.1f}." 
     f"\n-Uniswap: {Five_crypto_Sharpe_ratios[1]:.1f}."
     f"\n-Steller:{Five_crypto_Sharpe_ratios[2]:.1f}." 
     f"\n-Ethereum: {Five_crypto_Sharpe_ratios[3]:.1f}."
     f" \n-Litecoin: {Five_crypto_Sharpe_ratios[4]:.1f}."
     f"\nThe lower the Sharpe ratio, the lower the investment risk")
#Getting user preference over the coins to invest in.
print ("Select two coins from this list:")
first_coin=questionary.rawselect(
    "Select your first coin:",choices=["Bitcoin", "Uniswap", "Steller","Ethereum","Litecoin"]
).ask()
second_coin=questionary.rawselect(
    "Select your second coin:", choices=["Bitcoin", "Uniswap", "Steller","Ethereum","Litecoin"]
).ask()
# Getting the user's amount of investment.
investment=questionary.text("How much do you want to invest?").ask()
print (f"your choices are {first_coin} and {second_coin} and the amount of investment is ${investment}")
print ("......................................")
#Getting user's amount of investment.
print ("Choose the structure of your investment portfolio by determining the percentage of investment in each coin.\n Please give a number between 0 and 100 ")
first_coin_share=int(questionary.text(f"What percentage of this amount do you want to invest in {first_coin} ").ask())
second_coin_share=100-first_coin_share
answer=questionary.confirm(f"You want to invest {first_coin_share}% of your ${investment} in {first_coin} and {second_coin_share}% in {second_coin}.right?").ask()
#Setting up the first dataframe to start simulation, based on the user's first choice.
if first_coin=="Bitcoin":
    first_coin_df= Bitcoin
elif first_coin=="Uniswap":
    first_coin_df=Uniswap
elif first_coin=="Steller":
    first_coin_df=Steller
elif first_coin=="Ethereum":
    first_coin_df=Ethereum
elif first_coin=="Litecoin":
    first_coin_df=Litecoin
#Setting up the second dataframe to start simulation, based on the user's second choice.
if second_coin=="Bitcoin":
    second_coin_df= Bitcoin
elif second_coin=="Uniswap":
    second_coin_df=Uniswap
elif second_coin=="Steller":
    second_coin_df=Steller
elif second_coin=="Ethereum":
    second_coin_df=Ethereum
elif second_coin=="Litecoin":
    second_coin_df=Litecoin
#Concatinating the two dataframes to prepare the input for the Monter Carlo simulation
Two_coin_concat = pd.concat([first_coin_df, second_coin_df], axis=1, keys=[first_coin,second_coin], join="inner")
MC_Portfolio_weight = MCSimulation(
    portfolio_data = Two_coin_concat,
    weights= [first_coin_share/100,second_coin_share/100],
    num_simulation = 500 ,
    num_trading_days = 3*364
)
#Running Monte Carlo simulation
MC_Portfolio_weight.calc_cumulative_return()
Portfolio_table= MC_Portfolio_weight.summarize_cumulative_return()
lower_CI=round(Portfolio_table[8]*int(investment),2)
upper_CI=round(Portfolio_table[9]*int(investment),2)
#Giving the result of the simulation to inform the user about the potential benefit of investing in these cryptocurrencies.
print(f"There is a 95% chance that the profit of an initial investment of ${investment} in the selected portfolio"
      f" over the next 3 years would be in the range of ${lower_CI} and ${upper_CI}.")
