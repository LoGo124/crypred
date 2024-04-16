#Generic imports

#Specific imports
import streamlit as st

# Own imports
from src.classes.Frontend import CPFrontend

fend = CPFrontend(__name__)

st.title('🤖 ML CryPred')
st.image("src/resources/img/indice.jpg", channels="BGR", width=700)
with st.expander('About this app'):
    st.markdown('**What can this app do?**')
    st.info('ABOUT SECTION')

    st.markdown('**How to use the app?**')
    st.warning('HOW 2 USE SECTION')

    st.markdown('**Under the hood**')

    st.markdown('Data sets:')
    st.code('''DATA SETS SECTION''', language='markdown')

    st.markdown('Libraries used:')
    st.code('''LIBRARIES SECTION''', language='markdown')
