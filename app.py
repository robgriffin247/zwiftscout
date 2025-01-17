import streamlit as st
import polars as pl
import duckdb
import os

from zrapp.endpoints import get_club_riders
from zrapp.helpers import unpack_riders
from ui.inputs import group_builder, get_add_ids_input
from ui.helpers import add_new_riders_to_session_data, update_rider_data
from ui.figures import phenotypes_plot, power_curves_plot
from ui.tables import rider_table

st.set_page_config(page_title='ZwiftScout', page_icon=':bike:', layout='centered', )

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


scout_tab, add_tab = st.tabs(['Compare Riders', 'Add New Riders', ])


with add_tab:
    # Allow users to add missing riders or teams
    ids_input, input_type, get_riders_button = get_add_ids_input()
    add_new_riders_to_session_data(ids_input, input_type, get_riders_button)
    with duckdb.connect('data/zrapp.duckdb') as con:
        data = st.session_state['df_riders']
        con.sql(f'create or replace table core.riders as select * from data')


with scout_tab:
    # Allow users to choose focal riders
    grp1_cont, grp2_cont = st.columns(2, border=True)
    grp1_ids = group_builder(1, grp1_cont, st.session_state['df_riders'])
    grp2_ids = group_builder(2, grp2_cont, st.session_state['df_riders'])
    

    update_rider_data(grp1_ids, grp2_ids)

    # Display visuals only if 1+ riders are selected
    if len(grp1_ids+grp2_ids)>0:
        df_selected_riders = pl.concat([
            st.session_state['df_riders'].filter(pl.col('rider_id').is_in(grp1_ids)).with_columns(grp=1),
            st.session_state['df_riders'].filter(pl.col('rider_id').is_in(grp2_ids)).with_columns(grp=2),
        ])

        #st.dataframe(df_selected_riders)
        rider_table(df_selected_riders)
        phenotypes_plot(df_selected_riders)
        power_curves_plot(df_selected_riders)


