import numpy as np

from lumibot.entities import Asset
from lumibot.strategies import Strategy

from src.classes.Predictor import *

class BotStrategy(Strategy):
    """docstring for BotStrategy."""
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

class SwingWithPred(BotStrategy):
    """docstring for swingWithPred."""
    def __init__(
        self,
        *args,
        broker,
        product,
        predictor,
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

        self.product = product
        self.predictor = predictor
        
        self.iter_hist = []
        ...

    def initialize(self):
        self.predictor.predict()
        
    def on_trading_iteration(self):
        self.predictor.predict()
        print(self.predictor.pred_df)
        
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


class BuyHold(BotStrategy):

    def __init__(self):
        super(BotStrategy, self).__init__()

    def initialize(self):
        self.sleeptime = "1D"

    def on_trading_iteration(self):
        if self.first_iteration:
            symbol = "GOOG"
            price = self.get_last_price(symbol)
            quantity = self.cash // price
            order = self.create_order(symbol, quantity, "buy")
            self.submit_order(order)


class SwingHigh(BotStrategy):
    data = []
    order_number = 0

    def __init__(self):
        super(BotStrategy, self).__init__()

    def initialize(self):
        self.sleeptime = "10S"

    def on_trading_iteration(self):
        symbol ="BITC"
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


class Trend(BotStrategy):

    def __init__(self):
        super(BotStrategy, self).__init__()

    def initialize(self):
        signal = None
        start = "2022-01-01"

        self.signal = signal
        self.start = start
        self.sleeptime = "1D"
    # minute bars, make functions    

    def on_trading_iteration(self):
        bars = self.get_historical_prices("GLD", 22, "day")
        gld = bars.df
        #gld = pd.DataFrame(yf.download("GLD", self.start)['Close'])
        gld['9-day'] = gld['close'].rolling(9).mean()
        gld['21-day'] = gld['close'].rolling(21).mean()
        gld['Signal'] = np.where(np.logical_and(gld['9-day'] > gld['21-day'],
                                                gld['9-day'].shift(1) < gld['21-day'].shift(1)),
                                                "BUY", None)
        gld['Signal'] = np.where(np.logical_and(gld['9-day'] < gld['21-day'],
                                                gld['9-day'].shift(1) > gld['21-day'].shift(1)),
                                                "SELL", gld['Signal'])
        self.signal = gld.iloc[-1].Signal

        symbol = "GLD"
        quantity = 200
        if self.signal == 'BUY':
            pos = self.get_position(symbol)
            if pos is not None:
                self.sell_all()
                
            order = self.create_order(symbol, quantity, "buy")
            self.submit_order(order)

        elif self.signal == 'SELL':
            pos = self.get_position(symbol)
            if pos is not None:
                self.sell_all()

            order = self.create_order(symbol, quantity, "sell")
            self.submit_order(order)