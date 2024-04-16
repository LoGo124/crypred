#Generic imports
import csv

#Specific imports
from pandas import DataFrame
import streamlit as st

# Own imports
from src.classes.Frontend import CPFrontend
from src.classes.Bot import *
from src.classes.Broker import *

API_KEY = "PKUNQZ82EUWK8M6TNGUG"
SECRET_API_KEY = "aat3OlEw0oS9jwOpea2B4oFZYpTsNW3KywD29eP6"

def read() -> list:
    tmp_symbols = []
    with open("data/symbols_cryptocurrencys.csv", 'r', newline='\n') as archivo:
        lector_csv = csv.reader(archivo)
        tmp_csv = [row for row in lector_csv]
        tmp_symbols = DataFrame(tmp_csv[1:], columns=tmp_csv[0])
    return tmp_symbols

cryptoCurrencies: DataFrame = read()
fend = CPFrontend(__name__)

bots:list[Bot]
#bots = [CryptoCurrency(cry[1]["name"],cry[1]["symbol"]) for cry in cryptoCurrencies.iterrows()]
broker = Alpaca("Alpaca Broker 1", API_KEY, SECRET_API_KEY)
predictors = [Mosley(CryptoCurrency("Bitcoin","BTC-USD"), "Mosley 1","First predictor", auto_mode=True)]

bots = [Lilith(broker, predictors)]
for bot in bots:
    bot.show_on(web = True)