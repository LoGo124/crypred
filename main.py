import sys

from lumibot.entities import Asset
from config import ALPACA_CONFIG
from lumibot.brokers import Alpaca
from lumibot.strategies import Strategy
from lumibot.traders import Trader

from src.classes.Strategies import SwingWithPred
from src.classes.Product import *
from src.classes.Predictor import *

coins = {"BTC":"Bitcoin"}#,"ETH":"Ethereum"}

if __name__ == "__main__":
    broker = Alpaca(ALPACA_CONFIG)
    prods = [CryptoCurrency(coins[coin], coin) for coin in coins]
    preds = [Mosley(product=prod, interval="2m", changepoint_prior_scale=0.5, changepoint_range=0.8, show_mode="term") for prod in prods]
    strategies = [SwingWithPred(broker=broker, max_cash=1000, product=pred.product, predictor=pred, sleeptime="2M") for pred in preds]
    trader = Trader(strategies=strategies, logfile="logs/traders/log_test_01.log",debug=False)
    trader._set_logger()
    trader.run_all()
    #input("\n------STOP------\n")
    trader.stop_all()
