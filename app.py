import streamlit as st
import duckdb
import os

from zrapp.endpoints import get_club_riders
from zrapp.helpers import unpack_riders

st.set_page_config(page_title='ZwiftScout', 
                   page_icon=':bike:', 
                   layout='centered',
                   initial_sidebar_state='collapsed')

# Set up data for session 
if 'df_riders' not in st.session_state:
    # Create a basic dataset if no DB present
    if not os.path.exists('data/zrapp.duckdb'):
        with duckdb.connect('data/zrapp.duckdb') as con:
            con.sql('create schema if not exists core')
            data = unpack_riders(get_club_riders([20650, 2223]))#, 11818, 1]))
            con.sql(f'create or replace table core.riders as select * from data')
    
    # Load to session
    with duckdb.connect('data/zrapp.duckdb') as con:
        st.session_state['df_riders'] = con.sql('select * from core.riders').pl()



pg = st.navigation([
    st.Page('zs_pages/scout.py', title='Scout', icon=':material/person_search:'),
    st.Page('zs_pages/about.py', title='About', icon=':material/info:'),
    ])
pg.run()





