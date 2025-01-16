import streamlit as st
import duckdb
import polars as pl
from datetime import timedelta
from datetime import datetime as dt

from zrapp.endpoints import get_riders, get_club_riders
from zrapp.helpers import unpack_riders, update_selected_riders

def add_new_riders_to_session_data(ids_input, input_type, get_riders_button):
    if len(ids_input)>0 and get_riders_button:
            try:
                ids = [int(id) for id in ids_input.replace(',', '').split(' ') if id!='']
                if input_type=='Rider':
                    new_riders = unpack_riders(get_riders(ids))
                else:
                    new_riders = unpack_riders(get_club_riders(ids))
                st.session_state['df_riders'] = pl.concat([st.session_state['df_riders'], new_riders]).sort(['rider_id', 'last_update']).unique(subset='rider_id', keep='last')
            except:
                st.write(f'Please ensure your IDs are all valid {input_type.lower()} IDs and that IDs are all numeric values separated by commas, e.g. 1234, 4567, 8910')



def update_rider_data(grp1_ids, grp2_ids):
    col1, col2 = st.columns([3,6], vertical_alignment='center')

    if 'submit_updates_button' in st.session_state and st.session_state['submit_updates_button']:
        update_selected_riders(grp1_ids, grp2_ids)

    n_stale = st.session_state['df_riders'].filter(pl.col('rider_id').is_in(grp1_ids + grp2_ids)).filter(pl.col('last_update')<dt.now()-timedelta(days=3)).shape[0]

    if n_stale>0:
        with col1:
            submit_updates = st.button('Update Rider Data', 
                                    key='submit_updates_button',
                                    use_container_width=True,
                                    disabled=n_stale==0)
        with col2:
            if n_stale==1:
                st.write(f'{n_stale} rider has data >3 days old, feel free to refresh the data!')
            else:
                st.write(f'{n_stale} riders have data >3 days old, feel free to refresh the data!')
