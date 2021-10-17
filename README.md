# UWFinTech_Group3_Project1
## Analyzing five cryptocurrencies historical prices and providing guidance for investment
We have developed an appthat works through CLI which gives information about the cumulative return percentage since the beginning of 2021 and Sharpe ratios as an indicator of the risk associated with investing in each one of them. The app then takes the two cryptocurrencies that the user is interested in investing in, the amount of investment and the share of each coin in the portfolio of the investment and based on those information runs the Monte Carlo simulation to return the range of the prospect of investing in those coins after three years.
The list of the coins that the user can choose from is : Bitcoin (BTC), Ethereum (ETH), Litcoin (LTC), Uniswap (UNI), and Steller (XLM)

---

## Technologies
We use Python 3.5+ and along with several relevant libraries. We used Pandas which is included in Anaconda. Please go to: https://docs.anaconda.com/anaconda/install/ - For finding the proper installation guide.
The packages will be:
* [questionary](https://github.com/tmbo/questionary) - For interactive user prompts and dialogs
* [pandas] (https://github.com/pandas-dev/pandas)- For information and documentation
* [Numpy] (https://github.com/AhmetFurkanDEMIR/Numpy)- For information on the library and insights


---

## Installation Guide
Aside from installation of Anaconda, We need to install questionary and then import its library.
```python
    pip install questionary
```

---

## Usage
In order to see the graphs of the analysis go to the "Images" folder of the repository and find the Cumulative Return, the Daily Return and the comparative Sharpe Ratio plots of all the five cryptocurrencies.
To run the app, clone the repository on your PC, open Git Bash in the cloned folder and then type:
```console
    python CLI-project_1
```
You will see some information on the cumulative return of the 5 cryptocurrencies and their Sharpe ratios.
Then the program will ask you to choose two of them. In the next step, you will need to enter the amount of investment and at the last step, you will determine the structure of your portfolio. The program will ask your confirmation of the information, and then it will start simulating the historical data of the prices of these coins over the next three years and based on that, provides some insight on the amount of potential profit of this investment.

---

## Contributors
Somaye Nargesi
Swati Sobhadarshini
Jensen Eichenlaub

---

## License

MIT
