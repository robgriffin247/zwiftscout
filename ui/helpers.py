import streamlit as st
import polars as pl
import re
from datetime import timedelta
from datetime import datetime as dt

from zrapp.endpoints import get_riders, get_club_riders
from zrapp.helpers import unpack_riders, update_selected_riders

def string_to_ids(id_string):
        output = [int(i) for i in re.sub(r'\D+', ',', id_string).split(',') if i != '']
        return output

def add_new_riders_to_session_data(ids_input, input_type, get_riders_button):
    if len(ids_input)>0 and get_riders_button:
        try:
            ids = string_to_ids(ids_input)
            if input_type=='Rider':
                new_riders = unpack_riders(get_riders(ids))
            else:
                new_riders = unpack_riders(get_club_riders(ids))
            st.session_state['df_riders'] = pl.concat([st.session_state['df_riders'], new_riders]).sort(['rider_id', 'last_update']).unique(subset='rider_id', keep='last')
        except:
            st.write(f'Please ensure your IDs are all valid {input_type.lower()} IDs. Virtually any text input works here, as long as all numeric values are valid ID. For example "MMNKNENQWL313e;!MLM1123;MALSMD33" would fetch IDs 313, 1123 and 33. Check they are valid by finding the rider/club on zwiftpower or zwiftracing app. E.g. ID 4598636 looks like https://zwiftpower.com/profile.php?z=4598636')



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


