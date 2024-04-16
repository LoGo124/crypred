#Generic imports

#Specific imports
import streamlit as st

# Own imports
from src.classes.Frontend import CPFrontend
from src.classes.Broker import *

API_KEY = "PKUNQZ82EUWK8M6TNGUG"
SECRET_API_KEY = "aat3OlEw0oS9jwOpea2B4oFZYpTsNW3KywD29eP6"

fend = CPFrontend(__name__)

brokers:list[Broker]
brokers = [Alpaca("Alpaca Broker 1", API_KEY, SECRET_API_KEY)]
for broke in brokers:
    broke.show_on(True)