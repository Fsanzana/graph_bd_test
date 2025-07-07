import streamlit as st
from dotenv import load_dotenv
import os

load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

st.set_page_config(page_title='Graph Semantic App')

st.title('Graph Semantic App')

st.write('Seleccione una página en la barra lateral para empezar.')
