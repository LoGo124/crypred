#Generic imports
import csv

#Specific imports
from pandas import DataFrame
import streamlit as st

# Own imports
from src.classes.Frontend import CPFrontend
from src.classes.Product import *


def read() -> list:
    tmp_symbols = []
    with open("data/symbols_cryptocurrencys.csv", 'r', newline='\n') as archivo:
        lector_csv = csv.reader(archivo)
        tmp_csv = [row for row in lector_csv]
        tmp_symbols = DataFrame(tmp_csv[1:], columns=tmp_csv[0])
    return tmp_symbols

cryptoCurrencies: DataFrame = read()
fend = CPFrontend(__name__)

watchlist:list[Product]
#watchlist = [CryptoCurrency(cry[1]["name"],cry[1]["symbol"]) for cry in cryptoCurrencies.iterrows()]
watchlist = [CryptoCurrency("Bitcoin", "BTC-USD"), CryptoCurrency("Ethereum", "ETH-USD")]
for product in watchlist:
    product.show_on(on_web = True, expandable=True)