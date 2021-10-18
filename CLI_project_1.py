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
bitcoin = pd.DataFrame(c.get_product_historic_rates('BTC-USD', start = '2021-01-01T01:00:00', end = date.today() , granularity = 86400))
bitcoin.columns= ["Date","Open","High","Low","Close","Volume"]
bitcoin['Date'] = pd.to_datetime(bitcoin['Date'], unit='s')
bitcoin.set_index('Date', inplace=True)
bitcoin.sort_values(by='Date', ascending=True, inplace=True)
# Getting historical data of Uniswap price and putting it into data frame format in Pandas
uniswap= pd.DataFrame(c.get_product_historic_rates('UNI-USD', start = '2021-01-01T01:00:00', end = date.today() , granularity = 86400))
uniswap.columns= ["Date","Open","High","Low","Close","Volume"]
uniswap['Date'] = pd.to_datetime(uniswap['Date'], unit='s')
uniswap.set_index('Date', inplace=True)
uniswap.sort_values(by='Date', ascending=True, inplace=True)
# Getting historical data of Steller price and putting it into data frame format in Pandas
steller=  pd.DataFrame(c.get_product_historic_rates('XLM-USD', start = '2021-01-01T01:00:00', end = date.today() , granularity = 86400))
steller.columns= ["Date","Open","High","Low","Close","Volume"]
steller['Date'] = pd.to_datetime(steller['Date'], unit='s')
steller.set_index('Date', inplace=True)
steller.sort_values(by='Date', ascending=True, inplace=True)
# Getting historical data of Ethereum price and putting it into data frame format in Pandas
ethereum= pd.DataFrame(c.get_product_historic_rates('ETH-USD', start = '2021-01-01T01:00:00', end = date.today() , granularity = 86400))
ethereum.columns= ["Date","Open","High","Low","Close","Volume"]
ethereum['Date'] = pd.to_datetime(ethereum['Date'], unit='s')
ethereum.set_index('Date', inplace=True)
ethereum.sort_values(by='Date', ascending=True, inplace=True)
# Getting historical data of Litecoin price and putting it into data frame format in Pandas
litecoin= pd.DataFrame(c.get_product_historic_rates('LTC-USD', start = '2021-01-01T01:00:00', end = date.today() , granularity = 86400))
litecoin.columns= ["Date","Open","High","Low","Close","Volume"]
litecoin['Date'] = pd.to_datetime(litecoin['Date'], unit='s')
litecoin.set_index('Date', inplace=True)
litecoin.sort_values(by='Date', ascending=True, inplace=True)
#Concatinating five cryptocurrencies into one dataframe to start doing analysis on them.
five_Crypto= pd.concat([bitcoin, uniswap, steller, ethereum, litecoin], axis=1, keys= ["Bitcoin", "Uniswap", "Steller", "Ethereum", "Litecoin"])
# Slicing the closing price out of each dataframe
btc=bitcoin.loc[:,'Close']
uni=uniswap.loc[:,'Close']
xlm= steller.loc[:,'Close']
eth=ethereum.loc[:,'Close']
ltc= litecoin.loc[:,'Close']
#Adding all the closing prices to make one dataframe with five columns of closing prices and then titling each column with the relevant coin name.
five_crypto_closingprice=pd.concat([btc,uni,xlm,eth,ltc],axis=1)
five_crypto_closingprice.columns=['BTC','UNI','XLM','ETH','LTC']
# finding the percentage of change in the closing price for each coin.
five_crypto_daily_returns= five_crypto_closingprice.pct_change().dropna()
# Finding cumulative return of the price on each coin
five_crypto_cumulative_returns=(1+five_crypto_daily_returns).cumprod()
user_info_cumulative_return=five_crypto_cumulative_returns.tail(1)
#getting the percentage of change in each coin and showing them to the user.
all_cumulative_return=user_info_cumulative_return.values[0]*100
print(f"Here is the cumulative return of five popular cryptocurrencies from the beginning of 2021 \n - Bitcoin: {all_cumulative_return[0]:.1f}%." 
     f"\n- Uniswap: {all_cumulative_return[1]:.1f}%."
     f"\n-Steller:{all_cumulative_return[2]:.1f}%." 
     f"\n-Ethereum: {all_cumulative_return[3]:.1f}%."
     f" \n-Litecoin: {all_cumulative_return[4]:.1f}%."
     f"\n The higher the percentage of the cumulative return, the higher the investment profit")

trading_days=five_crypto_daily_returns.count()[1]+1
five_crypto_annual_average_return=five_crypto_daily_returns.mean()*trading_days
five_crypto_annual_std=five_crypto_daily_returns.std()* np.sqrt(trading_days)
five_crypto_sharpe_ratios=five_crypto_annual_average_return/five_crypto_annual_std
print("......................")
print(f"Here is the Sharpe ration of the above five popular cryptocurrencies \n-Bitcoin: {five_crypto_sharpe_ratios[0]:.1f}." 
     f"\n-Uniswap: {five_crypto_sharpe_ratios[1]:.1f}."
     f"\n-Steller:{five_crypto_sharpe_ratios[2]:.1f}." 
     f"\n-Ethereum: {five_crypto_sharpe_ratios[3]:.1f}."
     f" \n-Litecoin: {five_crypto_sharpe_ratios[4]:.1f}."
     f"\nThe lower the Sharpe ratio, the lower the investment risk")
#Getting user preference over the coins to invest in.
print ("Select two coins from this list:")
first_coin=questionary.rawselect(
    "Select your first coin:",choices=["bitcoin", "uniswap", "steller", "ethereum", "litecoin"]
).ask()
second_coin=questionary.rawselect(
    "Select your second coin:", choices=["bitcoin", "uniswap", "steller", "ethereum", "litecoin"]
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
if first_coin=="bitcoin":
    first_coin_df= bitcoin
elif first_coin=="uniswap":
    first_coin_df=uniswap
elif first_coin=="steller":
    first_coin_df=steller
elif first_coin=="ethereum":
    first_coin_df=ethereum
elif first_coin=="litecoin":
    first_coin_df=litecoin
#Setting up the second dataframe to start simulation, based on the user's second choice.
if second_coin=="bitcoin":
    second_coin_df= bitcoin
elif second_coin=="uniswap":
    second_coin_df=uniswap
elif second_coin=="steller":
    second_coin_df=steller
elif second_coin=="ethereum":
    second_coin_df=ethereum
elif second_coin=="litecoin":
    second_coin_df=litecoin
#Concatinating the two dataframes to prepare the input for the Monter Carlo simulation
two_coin_concat = pd.concat([first_coin_df, second_coin_df], axis=1, keys=[first_coin,second_coin], join="inner")
MC_portfolio_weight = MCSimulation(
    portfolio_data = two_coin_concat,
    weights= [first_coin_share/100,second_coin_share/100],
    num_simulation = 500 ,
    num_trading_days = 3*364
)
#Running Monte Carlo simulation
MC_portfolio_weight.calc_cumulative_return()
portfolio_table= MC_portfolio_weight.summarize_cumulative_return()
lower_ci=round(portfolio_table[8]*int(investment),2)
upper_ci=round(portfolio_table[9]*int(investment),2)
#Giving the result of the simulation to inform the user about the potential benefit of investing in these cryptocurrencies.
print(f"There is a 95% chance that the profit of an initial investment of ${investment} in the selected portfolio"
      f" over the next 3 years would be in the range of ${lower_ci} and ${upper_ci}.")
