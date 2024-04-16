import streamlit as st

from alpaca.trading.client import TradingClient

class Broker():
    """docstring for Broker."""
    def __init__(self, name: str, plataform: str, paper: bool):
        self.name = name
        self.plataform = plataform
        self.paper = paper
        self.string = str(self)

    def __str__(self) -> str:
        self.string = f"{'Name: ':30}{self.name}\n"
        self.string += f"{'Plataform: ':30}{self.plataform}\n"
        self.string += f"{'Is paper:':29} {str(self.paper)}\n"
        return self.string

    def show_on(self, on_web: bool = False):
        if on_web:
            st.subheader(self.name)
            st.text(str(self))
        pass


class Alpaca(Broker):
    """docstring for Alpaca."""
    def __init__(self, name: str, API_KEY: str, SECRET_KEY: str, paper = True):
        self.client = TradingClient(API_KEY, SECRET_KEY, paper=paper)
        self.account = dict(self.client.get_account())
        super(Alpaca, self).__init__(name, "Alpaca", paper=paper)

    def __str__(self) -> str:
        self.string = super().__str__()
        for k,v in self.account.items():
            self.string += f"{str(k)+':':30}{v}\n"
        return self.string

    def show_on(self, on_web: bool = False):
        super().show_on(on_web)
        if on_web:
            pass
        pass