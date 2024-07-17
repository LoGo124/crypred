import sys

from lumibot.entities import Asset
from config import ALPACA_CONFIG
from lumibot.brokers import Alpaca
from lumibot.strategies import Strategy
from lumibot.traders import Trader

from src.classes.Strategies import SwingWithPred
from src.classes.Product import *
from src.classes.Predictor import *

class SwingHigh(Strategy):
    data = []
    order_number = 0
    
    def __init__(
        self,
        *args,
        broker,
        minutes_before_closing=1,
        minutes_before_opening=60,
        sleeptime="1M",
        stats_file=None,
        risk_free_rate=None,
        benchmark_asset="SPY",
        backtesting_start=None,
        backtesting_end=None,
        quote_asset=Asset(symbol="USD", asset_type="forex"),
        starting_positions=None,
        filled_order_callback=None,
        name=None,
        budget=None,
        parameters={},
        buy_trading_fees=[],
        sell_trading_fees=[],
        force_start_immediately=False,
        discord_webhook_url=None,
        account_history_db_connection_str=None,
        strategy_id=None,
        discord_account_summary_footer=None,
        **kwargs,
    ):
        super().__init__(*args, broker=broker, minutes_before_closing=minutes_before_closing, minutes_before_opening=minutes_before_opening, sleeptime=sleeptime, stats_file=stats_file, risk_free_rate=risk_free_rate, benchmark_asset=benchmark_asset, backtesting_start=backtesting_start, backtesting_end=backtesting_end, quote_asset=quote_asset, starting_positions=starting_positions, filled_order_callback=filled_order_callback, name=name, budget=budget, parameters=parameters, buy_trading_fees=buy_trading_fees, sell_trading_fees=sell_trading_fees, force_start_immediately=force_start_immediately, discord_webhook_url=discord_webhook_url, account_history_db_connection_str=account_history_db_connection_str, strategy_id=strategy_id, discord_account_summary_footer=discord_account_summary_footer, **kwargs)
        ...

    def initialize(self):
        self.sleeptime = "10S"

    def on_trading_iteration(self):
        symbol ="GOOG"
        entry_price = self.get_last_price(symbol)
        self.log_message(f"Position: {self.get_position(symbol)}")
        self.data.append(self.get_last_price(symbol))

        if len(self.data) > 3:
            temp = self.data[-3:]
            if temp[-1] > temp[1] > temp[0]:
                self.log_message(f"Last 3 prints: {temp}")
                order = self.create_order(symbol, quantity = 10, side = "buy")
                self.submit_order(order)
                self.order_number += 1
                if self.order_number == 1:
                    self.log_message(f"Entry price: {temp[-1]}")
                    entry_price = temp[-1] # filled price
            if self.get_position(symbol) and self.data[-1] < entry_price * .995:
                self.sell_all()
                self.order_number = 0
            elif self.get_position(symbol) and self.data[-1] >= entry_price * 1.015:
                self.sell_all()
                self.order_number = 0


    def before_market_closes(self):
        self.sell_all()

coins = {"BTC":"Bitcoin"}#,"ETH":"Ethereum"}

if __name__ == "__main__":
    broker = Alpaca(ALPACA_CONFIG)
    prods = [CryptoCurrency(coins[coin], coin) for coin in coins]
    preds = [Mosley(product=prod, interval="1m", changepoint_prior_scale=0.5, changepoint_range=0.8, show_mode="term") for prod in prods]
    strategies = [SwingWithPred(broker=broker, max_cash=1000, product=pred.product, predictor=pred, sleeptime="1M") for pred in preds]
    trader = Trader(strategies=strategies, logfile="/home/sshadminonnando/crypred/logs/traders/log_test_01.log",debug=False)
    trader._set_logger()
    trader.run_all()
    #input("\n------STOP------\n")
    trader.stop_all()
