import pandas as pd
from datetime import datetime
import streamlit as st
from prophet import Prophet

from Product import *

class Predictor():
    """docstring for Predictor."""
    def __init__(self, product: Product, name = "Mosley", description = "", auto_mode = False):
        self.id_predictor = name + str(id(self))
        self.name = name
        self.description = description
        self.product = product
        self.product_class = str(type(product))

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
        
    def predict(self, on_web: bool = False):
        self.preds_done += 1
        if on_web:
            st.subheader("Prediction")
            st.line_chart(self.pred_df)

    def show_on(self, on_web: bool = False):
        if on_web:
            with st.container(border=True):
                st.subheader(self.name)
                st.info(self.description)
                
                if st.button("Predict", self.name):
                    self.predict(on_web=True)
                

class Mosley(Predictor):
    """docstring for Mosley.
    
        Upgrades:
            Intervalo autoajustado x una funcion en base al periodo de prediccion
    """
    def __init__(self, product:Product, name = "Mosley", description = "", interval: str = "1d", period: str = "max", auto_mode = False, changepoint_prior_scale = 0.5, changepoint_range = 0.8, df = None):
        self.changepoint_range = changepoint_range
        self.changepoint_prior_scale = changepoint_prior_scale
        self.interval = interval
        self.period = period
        super(Mosley, self).__init__(product, name, description, auto_mode)

    def gen_model(self):
        self.model = Prophet(changepoint_prior_scale=self.changepoint_prior_scale,
                    changepoint_range=self.changepoint_range)
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

    def collapse_on_web(self):
        pass
