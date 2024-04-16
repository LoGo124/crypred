import streamlit as st
import st_pages as stp

class CPFrontend():
    """docstring for ClassName."""
    def __init__(self, page):
        self.URL = "localhost:8502/"
        
        self.run_page_config()
        self.run_sidebar()

    def run_page_config(self):
        st.set_page_config(page_title='ML CryPred', page_icon='🤖')

    def run_sidebar(self):
        stp.show_pages_from_config()
        # setting sidebar options
        pages = {"Predictors" : "Predictors",
            "Brokers" : "Brokers",
            "Bots" : "Bots",
            "Watchlist" : "Watchlist",
        }
        
        # Side Nav Bar
        with st.sidebar:
            col_login, col_signup = st.columns(2)
            with col_login:
                st.button("**Login**",use_container_width=True)
            with col_signup:
                st.button("**Sign up**",use_container_width=True)

        return None