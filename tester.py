# Own imports
from src.classes.Product import *
from src.classes.Predictor import *
from src.classes.Broker import *
from src.classes.Bot import *

API_KEY = "PKUNQZ82EUWK8M6TNGUG"
SECRET_API_KEY = "aat3OlEw0oS9jwOpea2B4oFZYpTsNW3KywD29eP6"

broker = Alpaca("Alpaca",API_KEY, SECRET_API_KEY)
products = [CryptoCurrency("Bitcoin", "BTC-USD", "yfinance")]
bot = Lilith(broker, products, 1000)

products[0].get_hist(return_it=True, interval="1h")
pred = Mosley(products[0], interval="1h")
strat = SwingWithPred(products[0], pred)

pred.predict()

strat.on_trading_iteration()
#Generic imports
#import csv
#import requests
#from pandas import DataFrame

#Specific imports
#import streamlit as st
#import yfinance as yf
#import pytickersymbols

# Own imports
#from src.classes.Frontend import CPFrontend
#from src.classes.Product import *
#from src.classes.Predictor import *

#from pytickersymbols import PyTickerSymbols
#
#stock_data = PyTickerSymbols()
#countries = stock_data.get_all_countries()
#indices = stock_data.get_all_indices()
#industries = stock_data.get_all_industries()

#print(countries)
#print(indices)
#print(industries)

#print(stock_data.get_yahoo_ticker_symbols_by_index("IBEX 35"))



#CMCAP_API = "46260497-7823-4668-9439-c9116e9df096"

#predictors_list = [Mosley(CryptoCurrency("Bitcoin","BTC-USD"), "Mosley 1", auto_mode=True)]
#for pred in predictors_list:
#    pred.predict()

#def download():
#    # Obtener datos de criptomonedas desde la API de CoinMarketCap
#    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
#    params = {
#        'start': '1',
#        'limit': '200',  # Limitar a 100 criptomonedas para el ejemplo
#        'convert': 'USD'
#    }
#    headers = {
#        'X-CMC_PRO_API_KEY': '46260497-7823-4668-9439-c9116e9df096'  # Reemplazar con tu clave de API de CoinMarketCap
#    }
#
#    response = requests.get(url, params=params, headers=headers)
#    data = response.json()
#
#    # Procesar los datos para extraer los símbolos de las criptomonedas
#    if 'data' in data:
#        return data
#        symbols = [crypto['symbol'] for crypto in data['data']]
#    else:
#        print(data['error_message'])
#        return False
#
#def read(mode = "DataFrame") -> list:
#    tmp_symbols = []
#    with open("CryPred/crypred/data/symbols_cryptocurrencys.csv", 'r', newline='\n') as archivo:
#        lector_csv = csv.reader(archivo)
#        if mode == "list":
#            for fila in lector_csv:
#                tmp_symbols.append(fila)
#            return tmp_symbols
#        elif mode == "DataFrame":
#            tmp_csv = [row for row in lector_csv]
#            tmp_symbols = DataFrame(tmp_csv[1:], columns=tmp_csv[0])
#            return tmp_symbols
#
#def write(tmp_symbols) -> bool:
#    with open("CryPred/crypred/data/symbols_cryptocurrencys.csv", 'w', newline='\n') as archivo:
#        if type(tmp_symbols) == type(list()):
#            escritor_csv = csv.writer(archivo)
#            for e in tmp_symbols:
#                escritor_csv.writerow(e)
#        elif type(tmp_symbols) == type(DataFrame()):
#            archivo.write(tmp_symbols.to_csv(index=False))
#        return True
#
#
#claves_deseadas = {
#'name',
#'symbol',
#'quote',
#'max_supply',
#'total_supply',
#'infinite_supply'
#}
#
#for_save = []
#data = download()
#for c in data['data']:
#    tmp_data = {clave: c[clave] for clave in claves_deseadas}
#
#    tmp_data['price'] = tmp_data.pop('quote')['USD']['price']
#
#    for_save.append(tmp_data)
#for_save = DataFrame(for_save, columns=for_save[0].keys(), index=[cry['symbol'] for cry in for_save])
#write(for_save)


#print(yf.download("AMZN"))
#print(yf.Tickers("AMZN GOOG"))
#print(yf.Tickers("AMZN GOOG").history())

#cryptoCurrencies:DataFrame = read()
#
#watchlist:list[Product]
#watchlist = [CryptoCurrency(cry[1]["name"],cry[1]["symbol"]) for cry in cryptoCurrencies.iterrows()]
#for product in watchlist:
#    print(product)