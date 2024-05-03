import pandas as pd
from datetime import datetime
import streamlit as st
from prophet import Prophet

from src.classes.Product import *

class Predictor():
    """docstring for Predictor."""
    def __init__(self, product: Product, name: str = "Mosley", description: str = "", show_mode: str = "web", auto_mode: bool = False):
        #self.id_predictor = name + str(id(self))
        self.name = name
        self.description = description
        self.product = product
        self.product_class = str(type(product))
        self.show_mode = show_mode.lower()

        self.have_model = False
        self.fit_period = 180
        self.fit_interval = 1
        self.fits_done = 0
        self.pred_days = 1
        self.preds_done = 0
        self.container = False

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
        
    def predict(self, st_container = False):
        self.preds_done += 1
        if not st_container:
            st_container = self.container
        if self.show_mode == "web":
            st_container.subheader("Prediction")
            #st_container.line_chart(self.pred_df)

    def show_on(self):
        if self.show_mode == "web":
            self.container = st.expander("📈 " + self.name, expanded=True)
            self.container.info(self.description)
        elif self.show_mode == "term":
            print(f"Name: {self.name}\nDescription: {self.description}")

class Mosley(Predictor):
    """docstring for Mosley.
    
        Upgrades:
            Intervalo autoajustado x una funcion en base al periodo de prediccion
    """
    def __init__(self, name = "Mosley", description = "", product : CryptoCurrency = None, interval: str = "1d", period: str = "max", changepoint_prior_scale = 0.5, changepoint_range = 0.8, df = None, show_mode: str = "web", auto_mode = False):
        self.changepoint_range = changepoint_range
        self.changepoint_prior_scale = changepoint_prior_scale
        
        self.model = Prophet(changepoint_prior_scale=self.changepoint_prior_scale, changepoint_range=self.changepoint_range, n_changepoints=100)
        
        self.interval = interval
        
        if auto_mode and not product:
            raise ValueError("Can't use auto_mode without a correct atribute product")
        
        super(Mosley, self).__init__(product, name, description, show_mode, auto_mode)

    def gen_model(self, changepoint_prior_scale: float = None, changepoint_range: float = None):
        if changepoint_prior_scale:
            self.changepoint_prior_scale = changepoint_prior_scale
        if changepoint_range:
            self.changepoint_range = changepoint_range
        self.model = Prophet(changepoint_prior_scale=self.changepoint_prior_scale, changepoint_range=self.changepoint_range)
        return super(Mosley, self).gen_model()

    def fit_model(self, interval: str = None, fit_df = None):
        if interval:
            self.interval = interval

        if fit_df:
            self.fit_df = fit_df
        else:
            self.fit_df = self.product.get_hist(self.interval, return_it=True)

        if self.fits_done:
            self.gen_model()
        self.model.fit(self.fit_df)
        return super(Mosley, self).fit_model()

    def predict(self, days_predicted: int = 30, interval: str = None, return_df: bool = False, st_container = False):
        if not st_container:
            st_container = self.container
        st_container.prog_bar = self.container.progress(0,text="Checking model...")

        if interval:
            self.interval = interval

        if not self.have_model:
            st_container.prog_bar.progress(0, text="Generating model...")
            self.gen_model(self.changepoint_prior_scale, self.changepoint_range)

        st_container.prog_bar.progress(10, text="Checking train...")
        if self.fits_done <= 0 or interval:
            st_container.prog_bar.progress(20, text="Training model...")
            self.fit_model()

        st_container.prog_bar.progress(30, text="Preparing DataFrame...")

        self.pred_days = days_predicted
        future = self.model.make_future_dataframe(periods=days_predicted * 24, freq = "h") #Posible mejora de Mosley

        st_container.prog_bar.progress(50, text="Predicting...")
        predictions = self.model.predict(future)
        #predictions = predictions[predictions['ds'].dt.dayofweek < 5]
        self.pred_df = predictions[['ds','trend','yhat','yhat_lower','yhat_upper']]
        self.pred_df['y'] = self.product.hist_df['y']
        self.pred_df = self.pred_df.set_index('ds')

        st_container.prog_bar.progress(80, text="Predicting...")
        super().predict(st_container = st_container)
        if self.show_mode == "web":
            st_container.prog_bar.progress(90, text="Showing...")
            st_container.write(f"Days predicted : {self.pred_days}\nShowed days : {(self.pred_days * 10)}")
            st_container.line_chart(self.pred_df)
            fig_components = self.model.plot_components(predictions)
            st_container.pyplot(fig_components)
            st_container.prog_bar.progress(100, text="Finished")

        if return_df:
            return self.pred_df

    def show_on(self):
        super(Mosley, self).show_on()
        if self.show_mode == "web":
            modelTab, trainingTab ,predictionTab = self.container.tabs(["Model Editor", "Train Editor", "Prediction"])

            #Model Tab
            self.changepoint_range = modelTab.number_input('changepoint range', min_value=0.1, max_value=0.99, value=self.changepoint_range, step=0.1, on_change=self.gen_model)
            self.changepoint_prior_scale = modelTab.number_input('changepoint prior scale', min_value=0.5, max_value=5.0, value=self.changepoint_prior_scale, step=0.1, on_change=self.gen_model)

            #Interval/period selectors
            intervalOptions = ['1m', '2m', '5m', '15m', '30m', '1h', '90m', '1d', '5d', '1wk', '1mo', '3mo']
            self.interval = trainingTab.selectbox('interval', options=intervalOptions, index=(intervalOptions.index(self.interval) if self.interval in intervalOptions else 5), label_visibility="hidden", key=str(id(self))+"interval", on_change=self.fit_model)
            trainingTab.selectbox('period', options=['max'], index=0, label_visibility="hidden", key=str(id(self))+"period", disabled=True)

            self.fit_model()
            trainingTab.dataframe(self.fit_df)

            #Predict Tab
            days_predicted = predictionTab.number_input('Prediction days', min_value=1, max_value=180, value=10, step=1)
            with predictionTab:
                self.predict(days_predicted=days_predicted, st_container=predictionTab)

        elif self.show_mode == "term":
            if input("Want perdict? [y/n] : ").lower() == "y":
                self.predict()
