import pandas as pd
from datetime import datetime
import streamlit as st
from prophet import Prophet

from src.classes.Product import *

class Predictor():
    """docstring for Predictor."""
    def __init__(self, product: Product, name: str = "Mosley", description: str = "", show_mode: str = "web", auto_mode: bool = False):
        self.id_predictor = name + str(id(self))
        self.name = name
        self.description = description
        self.product = product
        self.product_class = str(type(product))
        self.show_mode = show_mode.lower()

        self.have_model = False
        self.fits_done = 0
        self.preds_done = 0

        if auto_mode:
            self.fit_df = self.product.get_hist(return_it=True)
            self.gen_model()
            self.fit_model()
            self.predict()
        else:
            self.fit_df = None
            self.pred_df = None

    def gen_model(self):
        self.fits_done = 0
        self.have_model = True
        
    def fit_model(self):
        self.fits_done += 1
        
    def predict(self):
        self.preds_done += 1
        if self.show_mode == "web":
            st.subheader("Prediction")
            st.line_chart(self.pred_df)

    def show_on(self):
        if self.show_mode == "web":
            with st.container(border=True):
                st.subheader(self.name)
                st.info(self.description)
                if st.button("Edit model"):
                    changepoint_range = st.sidebar.number_input('changepoint_range', min_value=0.1, max_value=0.99, value=0.5, step=0.1)
                    changepoint_prior_scale = st.sidebar.number_input('changepoint_prior_scale', min_value=0.5, max_value=5.0, value=1.0, step=0.1)
                    if st.button("Re-Generate model"):
                        self.gen_model()
                if st.button("Predict", self.name):
                    self.predict()
        elif self.show_mode == "term":
            print(f"Name: {self.name}\nDescription: {self.description}")
            if input("Want perdict? [y/n] : ").lower() == "y":
                self.predict()

    def expand_on(self):
        ...

    def collapse_on(self):
        ...

class Mosley(Predictor):
    """docstring for Mosley.
    
        Upgrades:
            Intervalo autoajustado x una funcion en base al periodo de prediccion
    """
    def __init__(self, name = "Mosley", description = "", product : CryptoCurrency = None, interval: str = "1d", period: str = "max", changepoint_prior_scale = 0.5, changepoint_range = 0.8, df = None, show_mode: str = "web", auto_mode = False):
        self.changepoint_range = changepoint_range
        self.changepoint_prior_scale = changepoint_prior_scale
        self.interval = interval
        self.period = period
        
        if auto_mode and not product:
            raise ValueError("Can't use auto_mode without a correct atribute product")
        
        super(Mosley, self).__init__(product, name, description, show_mode, auto_mode)

    def gen_model(self, changepoint_prior_scale: float, changepoint_range: float):
        self.model = Prophet(changepoint_prior_scale=changepoint_prior_scale, changepoint_range=changepoint_range)
        return super(Mosley, self).gen_model()

    def fit_model(self, period: str, interval: str, fit_df = None):
        if fit_df:
            self.fit_df = fit_df
        else:
            self.fit_df = self.product.get_hist(interval = interval, period = period, return_it=True)
        self.model.fit(self.fit_df)
        return super(Mosley, self).fit_model()

    def predict(self, days_predicted: int = 30, return_df: bool = False, on_web: bool = False):
        if not self.have_model:
            self.gen_model()

        if self.fits_done <= 0:
            if int(3000 / (days_predicted * 24 * 60)) > 1:
                interval = "1m"
                period = "2d"
            elif int(3000 / (days_predicted * 24 * 30)) > 1:
                interval = "2m"
                period = "4d"
            elif int(3000 / (days_predicted * 24 * 12)) > 1:
                interval = "5m"
                period = "10d"
            elif int(3000 / (days_predicted * 24 * 4)) > 1:
                interval = "15m"
                period = "30d"
            elif int(3000 / (days_predicted * 24 * 2)) > 1:
                interval = "30m"
                period = "60d"
            elif int(3000 / (days_predicted * 24)) > 1:
                interval = "1h"
                period = "3mo"
            elif int(3000 / (days_predicted * 16)) > 1:
                interval = "90m"
                period = "6mo"
            elif int(3000 / days_predicted) > 1:
                interval = "1d"
                period = "max"
            else:
                interval = "1d"
                period = "max"

            self.fit_model(period, interval)

        future = self.model.make_future_dataframe(periods=days_predicted * 24 * 60, freq = "min") #Posible mejora de Mosley

        predictions = self.model.predict(future)
        #predictions = predictions[predictions['ds'].dt.dayofweek < 5]
        self.pred_df = predictions[['ds','trend','yhat','yhat_lower','yhat_upper']]
        self.pred_df['y'] = self.product.hist_df['y']
        self.pred_df = self.pred_df.set_index('ds')

        super().predict(on_web)
        if on_web:
            fig_components = self.model.plot_components(predictions)
            st.pyplot(fig_components)

            #see your data
            st.dataframe(self.product.ticker_df)
            
            st.button("Hide data and graph")
            if st.button:
                self.collapse_on_web()
        if return_df:
            return self.pred_df

    def collapse_on(self):
        pass
