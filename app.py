import streamlit as st
import polars as pl
import duckdb
import os

from zrapp.endpoints import get_riders, get_club_riders
from zrapp.helpers import unpack_riders, update_selected_riders
from ui.inputs import group_builder, get_add_ids_input
from ui.helpers import add_new_riders_to_session_data, update_rider_data


if 'df_riders' not in st.session_state:
    if not os.path.exists('data/zrapp.duckdb'):
        with duckdb.connect('data/zrapp.duckdb') as con:
            con.sql('create schema if not exists core')
            data = unpack_riders(get_club_riders([20650, 2223]))#, 11818, 1]))
            con.sql(f'create or replace table core.riders as select * from data')
    
    with duckdb.connect('data/zrapp.duckdb') as con:
        st.session_state['df_riders'] = con.sql('select * from core.riders').pl()



scout_tab, add_tab = st.tabs(['Compare Riders', 'Add New Riders'])


with add_tab:

    ids_input, input_type, get_riders_button = get_add_ids_input()
    add_new_riders_to_session_data(ids_input, input_type, get_riders_button)
    with duckdb.connect('data/zrapp.duckdb') as con:
        data = st.session_state['df_riders']
        con.sql(f'create or replace table core.riders as select * from data')


with scout_tab:

    grp1_cont, grp2_cont = st.columns(2, border=True)
    grp1_ids = group_builder(1, grp1_cont, st.session_state['df_riders'])
    grp2_ids = group_builder(2, grp2_cont, st.session_state['df_riders'])

    update_rider_data(grp1_ids, grp2_ids)

    if len(grp1_ids+grp2_ids)>0:
        df_selected_riders = pl.concat([
            st.session_state['df_riders'].filter(pl.col('rider_id').is_in(grp1_ids)).with_columns(grp=1),
            st.session_state['df_riders'].filter(pl.col('rider_id').is_in(grp2_ids)).with_columns(grp=2),
        ])

        st.dataframe(df_selected_riders)

