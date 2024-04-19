import streamlit as st
from lumibot.strategies import Strategy
from lumibot.traders import Trader

from src.classes.Strategies import *
from src.classes.Predictor import *
from src.classes.Broker import *
from src.classes.Product import *

class Bot(Trader):
    """docstring for Bot."""
    def __init__(self, broker: Broker, products: list[Product], assigned_cash: int, name : str = "Bot", descrption : str = "Default Bot"):
        super(Bot, self).__init__(logfile="/home/ignuser/PWZ/Python_WZ/CryPred/crypred/logs/traders/log-01")
        self.name = name
        self.descrption = descrption
        self.broker = broker
        self.products = products
        self.status = "__init__"

        if self.check_cash(assigned_cash):
            self.cash = assigned_cash

        self.profit = 0
        self.string = str(self)

    def __str__(self) -> str:
        self.string = f"{'Name: ':30}{self.name}\n"+\
                    f"{'Description: ':30}{self.descrption}\n"+\
                    f"{'Broker: ':30}{self.broker.name}\n"+\
                    f"{'Cash: ':30}{self.cash}"
        return self.string

    def show_on(self, web: bool = False):
        if web:
            with st.container(border=True):
                st.subheader(self.name)
                st.info(self.descrption)
                if st.button("Start", f"Start {self.name}"):
                    with st.container(border=True):
                        self.start()

    def start(self):
        cash_for = self.cash / len(self.products)
        for product in self.products:
            pred = Mosley(product)
            self.add_strategy(SwingWithPred(pred))
        self.run_all()

    def stop_all(self):
        super(Bot, self).stop_all()
    
    def pause(self):
        pass

    def play(self):
        pass
    
    def check_cash(self, cash: int):
        pass


class Lilith(Bot):
    """docstring for Lilith."""
    def __init__(self, broker : Broker, products: list[Product], assigned_cash: int, name: str = "Lilith", descrption: str = "First bot, use de recived product to swing using the yhat lower & upper parameters as triger to buy & sell"):
        super(Lilith, self).__init__(broker, products, assigned_cash, name, descrption)
        

    def __str__(self) -> str:
        self.string = super(Lilith, self).__str__()
        self.string += f"\n-Watched products ({len(self.products)})-\n"
        for prod in self.products:
            self.string += f"{'Name: ':30}{prod.name}\n"
            self.string += f"{'Symbol: ':30}{prod.tickerSymbol}\n"
            self.string += f"{'Price: ':30}{prod.get_current_price(True)}\n"
        return self.string
    
    def show_on(self, web: bool = False):
        super().show_on(web)
        

    def start(self):
        pass

    def stop_all(self):
        super(Lilith, self).stop_all()

    def pause(self):
        pass

    def play(self):
        pass
    
    def check_cash(self, cash: int):
        if cash < int(self.broker.account["cash"]):
            return True
        else:
            return False