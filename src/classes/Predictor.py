import pandas as pd
import streamlit as st
from prophet import Prophet

from src.classes.Product import *

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
    """docstring for Mosley."""
    def __init__(self, product:Product, name = "Mosley", description = "", interval: str = "1d", auto_mode = False, changepoint_prior_scale = 0.5, changepoint_range = 0.8, df = None):
        self.changepoint_range = changepoint_range
        self.changepoint_prior_scale = changepoint_prior_scale
        self.interval = interval
        super(Mosley, self).__init__(product, name, description, auto_mode)

    def gen_model(self):
        self.model = Prophet(changepoint_prior_scale=self.changepoint_prior_scale,
                    changepoint_range=self.changepoint_range)
        return super(Mosley, self).gen_model()

    def fit_model(self, fit_df = None):
        if fit_df:
            self.fit_df = fit_df
        else:
            self.fit_df = self.product.get_hist(self.interval, return_it=True)
        self.model.fit(self.fit_df)
        return super(Mosley, self).fit_model()

    def predict(self, on_web: bool = False, period = 30, interval: str = "1d"):
        if not (self.have_model) or interval != self.interval:
            self.gen_model()

        if self.fits_done <= 0:
            self.fit_model()

        future = self.model.make_future_dataframe(periods=period)

        predictions = self.model.predict(future)
        predictions = predictions[predictions['ds'].dt.dayofweek < 5]
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
        
    def collapse_on_web(self):
        pass
