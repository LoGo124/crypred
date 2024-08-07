import datetime

from config import ALPACA_CONFIG
from lumibot.brokers import Alpaca
from lumibot.traders import Trader

from src.classes.Strategies import SwingWithPred
from src.classes.Product import *
from src.classes.Predictor import *

coins = {"BTC":"Bitcoin"}#,"ETH":"Ethereum"}

if __name__ == "__main__":
    broker = Alpaca(ALPACA_CONFIG)
    prods = [CryptoCurrency(coins[coin], coin) for coin in coins]
    preds = [Mosley(product=prod, interval="1m", changepoint_prior_scale=1, changepoint_range=0.99, show_mode="term") for prod in prods]
    strategies = [SwingWithPred(broker=broker, max_cash=1000, product=pred.product, predictor=pred, sleeptime="1M") for pred in preds]
    trader = Trader(strategies=strategies, logfile=f"logs/traders/log_test_{datetime.now()}.log",debug=False)
    trader._set_logger()
    trader.run_all()
    #input("\n------STOP------\n")
    trader.stop_all()