#Generic imports

#Specific imports
#import streamlit as st

# Own imports
from src.classes.Frontend import CPFrontend
from src.classes.Product import CryptoCurrency
from src.classes.Predictor import Mosley

fend = CPFrontend(__name__)
predictors_list = [Mosley("Mosley","First predictor", CryptoCurrency("Bitcoin","BTC"))]
for pred in predictors_list:
    pred.show_on()