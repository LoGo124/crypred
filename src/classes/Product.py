import datetime as dt
import pandas as pd

import yfinance as yf
import streamlit as st


class Product():
    """docstring for Product."""
    def __init__(self, name: str, tickerSymbol: str, input_mode = "yfinance", show_mode: str = "web"):
        self.name = name
        self.assetType: str
        self.tickerSymbol = tickerSymbol
        self.pairSymbol = tickerSymbol + "-USD"
        self.input_mode = input_mode
        self.show_mode = show_mode

        match self.input_mode:
            case "yfinance":
                self.ticker = yf.Ticker(self.pairSymbol)

        self.lastUpdate = None
        self.current_price:float = 0
        self.hist_df = None
        self.container = False
        self.h_period = 180
        self.h_interval = 1
        
        self.string:str = str(self)

    def __str__(self, update_data:bool = False) -> str:
        if update_data:
            self.get_current_price()
        self.string = f"{'Name: ':30}{self.name}\n"+\
                    f"{'Symbol: ':30}{self.tickerSymbol}\n"+\
                    f"{'Input Mode: ':30}{self.input_mode}\n"
        if self.current_price:
            self.string += f"{'Current Price: ':30}{self.current_price}\n"
        return self.string

    def get_hist(self, interval: str = "1d", return_it: bool = False):
        match self.input_mode:
            case "yfinance":
                best_period_for_this = {
                    "1m": "max",
                    "2m": "60d",
                    "5m": "60d",
                    "15m" : "60d",
                    "30m" : "60d",
                    "1h" : "730d",
                    "90m" : "60d",
                    "1d" : "max",
                    "5d" : "max",
                    "1wk" : "max",
                    "1mo" : "max",
                    "3mo" : "max"
                }
                period = best_period_for_this[interval]
                self.ticker_df = self.ticker.history(interval=interval, period = period)
                #yf.download("BTC-USD", period="1d", interval="10m")

                if self.ticker_df.empty:
                    return False

                tmp_df = self.ticker_df['Close']
                tmp_df = tmp_df.reset_index()
                tmp_df = tmp_df.rename(columns={'Date': 'ds', 'Datetime' : 'ds', 'Close': 'y'})
                tmp_df['ds'] = tmp_df['ds'].dt.tz_localize(None)

                self.hist_df = tmp_df

        self.get_current_price()
        self.lastUpdate = dt.datetime.now()
        if return_it:
            return self.hist_df
        else:
            return True

    def get_current_price(self, return_it: bool = False):
        match self.input_mode:
            case "yfinance":
                tmp_ticker_df = self.ticker.history(period='1d', interval = '1m')
                self.current_price = tmp_ticker_df["Close"].iloc[-1]
        self.lastUpdate = dt.datetime.now()
        if return_it:
            return self.current_price

    def show_on(self):
        if self.show_mode == "web":
            self.container = st.expander(self.name, expanded=True)
            self.container.text(str(self))

            #Interval/period selectors
            intervalOptions = ['1m', '2m', '5m', '15m', '30m', '1h', '90m', '1d', '5d', '1wk', '1mo', '3mo']
            interval = self.container.selectbox('interval', options=intervalOptions, index=5, label_visibility="hidden", key=str(id(self))+"interval")
            self.container.selectbox('period', options=['max'], index=0, label_visibility="hidden", key=str(id(self))+"period", disabled=True)

            self.get_hist(interval=interval)
            self.get_current_price()
            self.container.line_chart(self.hist_df, x="ds", y="y")
            #self.container.update(state="complete")
            #self.container.dataframe(self.hist_df)


class Currency(Product):
    """docstring for Currency."""
    def __init__(self, name: str, tickerSymbol: str, input_mode = "yfinance", show_mode: str = "web"):
        super(Currency, self).__init__(name, tickerSymbol, input_mode, show_mode)
        self.assetType = "forex"

class Company(Product):
    """docstring for Company."""
    def __init__(self, name: str, tickerSymbol: str, input_mode = "yfinance", show_mode: str = "web"):
        super(Company, self).__init__(name, tickerSymbol, input_mode, show_mode)
        self.assetType = "stock"
        
class CryptoCurrency(Currency):
    """docstring for CryptoCurrency."""
    def __init__(self, name: str, tickerSymbol: str, input_mode = "yfinance", show_mode: str = "web"):
        super(CryptoCurrency, self).__init__(name, tickerSymbol, input_mode=input_mode, show_mode=show_mode)
        self.assetType = "crypto"