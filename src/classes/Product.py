import datetime as dt
import pandas as pd

import yfinance as yf
import streamlit as st



class Product():
    """docstring for Product."""
    def __init__(self, name: str, tickerSymbol: str, input_mode = "yfinance"):
        self.name = name
        self.tickerSymbol = tickerSymbol
        self.input_mode = input_mode

        match self.input_mode:
            case "yfinance":
                self.ticker = yf.Ticker(self.tickerSymbol)
                if 'symbol' not in self.ticker.info:
                    return False


        self.lastUpdate = None
        self.current_price:float = 0
        self.hist_df = None
        
        self.string:str = str(self)

    def __str__(self, update_data:bool = False) -> str:
        if update_data:
            self.get_hist()
            self.get_current_price()
        self.string = f"{'Name: ':30}{self.name}\n"+\
                    f"{'Symbol: ':30}{self.tickerSymbol}\n"+\
                    f"{'Input Mode: ':30}{self.input_mode}\n"
        if self.current_price:
            self.string += f"{'Current Price: ':30}{self.current_price}\n"
        return self.string

    def get_hist(self, period: str = "max", interval: str = "1d", return_it: bool = False):
        match self.input_mode:
            case "yfinance":
                if interval == "1h":
                    period = "2y"
                elif interval == "30m":
                    period = "60d"
                elif interval == "15m":
                    period = "1mo"
                elif interval == "10m":
                    period = "20d"
                self.ticker_df = self.ticker.history(period=period, interval=interval)
                #yf.download("BTC-USD", period="1d", interval="10m")

                if self.ticker_df.empty:
                    return False

                tmp_df = self.ticker_df['Close']
                tmp_df = tmp_df.reset_index()
                tmp_df = tmp_df.rename(columns={'Date': 'ds', 'Close': 'y'})
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
                tmp_ticker_df = self.ticker.history(period='1d')
                self.current_price = tmp_ticker_df["Close"].iloc[-1]
        self.lastUpdate = dt.datetime.now()
        if return_it:
            return self.current_price

    def show_on(self, on_web: bool = False, expandable: bool = False):
        if on_web:
            with st.container(border=True):
                st.subheader(self.name)
                st.text(str(self))
                if expandable:
                    if st.button(f"See graph", self.name):
                        self.expand_on_web()

    def expand_on_web(self):
        self.get_hist()
        self.get_current_price()
        st.line_chart(self.hist_df, x="ds", y="y")
        st.dataframe(self.hist_df)
        st.button("Hide data and graph")
        if st.button:
            self.collapse_on_web()
        
    def collapse_on_web(self):
        pass


class Currency(Product):
    """docstring for Currency."""
    def __init__(self, name: str, tickerSymbol: str, input_mode = "yfinance"):
        super(Currency, self).__init__(name, tickerSymbol, input_mode)

class Company(Product):
    """docstring for Company."""
    def __init__(self, name: str, tickerSymbol: str, input_mode = "yfinance"):
        super(Company, self).__init__(name, tickerSymbol, input_mode)
        
class CryptoCurrency(Currency):
    """docstring for CryptoCurrency."""
    def __init__(self, name: str, tickerSymbol: str, input_mode = "yfinance"):
        super(CryptoCurrency, self).__init__(name, tickerSymbol, input_mode)