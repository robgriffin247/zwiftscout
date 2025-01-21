import streamlit as st
import polars as pl
from ui.helpers import string_to_ids

def group_builder(id, cont, data):
    

    
    with cont:
        
        st.write(f'Team {id}')
        club_select = st.container()
        riders_select = st.container()

        def clear_ids():
            if (f'grp{id}_riders' in st.session_state):
                st.session_state.pop(f'grp{id}_riders')

        bulk = st.toggle('Bulk Select', on_change=clear_ids, key=f'grp{id}_bulk',value=False, help='Got IDs? Paste them in rather than using the rider search & select!')

        if bulk:
            grp_riders = riders_select.text_input('Rider IDs',
                                                  key=f'grp{id}_riders',
                                                  help='Paste IDs - you can paste ids or URLs, pretty much anything, as long as all numbers are IDs and they is something - a space, a comma, a letter... whatever - between the IDs! e.g. 1234jnaskjd5678 will load 1234 and 5678')
            grp_ids = string_to_ids(grp_riders)

        else:

            club_select.multiselect('Club(s)',
                        key=f'grp{id}_clubs',
                        options=data['club'].unique().sort())

            grp_rider_choices = data.filter((pl.col('club').is_in(st.session_state[f'grp{id}_clubs']) if (f'grp{id}_clubs' in st.session_state and len(st.session_state[f'grp{id}_clubs'])>0) else True) |
                                                                (pl.col('rider').is_in(st.session_state[f'grp{id}_riders']) if (f'grp{id}_riders' in st.session_state and len(st.session_state[f'grp{id}_riders'])>0) else False))['rider']


            grp_riders = riders_select.multiselect('Rider(s)', 
                                        max_selections=10,
                                        key=f'grp{id}_riders', 
                                        options=grp_rider_choices,
                                        default=st.session_state[f'grp{id}_riders'] if (f'grp{id}_riders' in st.session_state) and (st.session_state[f'grp{id}_riders']!='') else None)

            grp_ids = [int(i.split(']')[0].split('[')[1]) for i in grp_riders]
            
    return grp_ids


def get_add_ids_input():
    ids_input = st.text_input('IDs', 
                              key='ids_input',
                              placeholder='12345, 23456, 34567',
                              help='Enter one or more IDs. Tip &mdash; you can enter numbers, zwiftpower and zwiftracing.app urls, anything as long as all numbers are valid IDs. Find ID numbers in the ZwiftPower and ZwiftRacing app URLs, e.g. https://zwiftpower.com/profile.php?z=4598636')
    
    col1, col2, _ = st.columns([4,4,8], vertical_alignment='bottom')
    
    with col1:
        input_type = st.selectbox('ID Type', ['Rider', 'Club'])
    with col2:
        get_riders_button = st.button('Get Riders!', use_container_width=True)

    return ids_input, input_type, get_riders_button
    
"""
def group_builder(id, cont, data):
    with cont:
        
        st.write(f'Team {id}')

        st.multiselect('Club(s)',
                    key=f'grp{id}_clubs',
                    options=data['club'].unique().sort())

        grp_rider_choices = data.filter((pl.col('club').is_in(st.session_state[f'grp{id}_clubs']) if (f'grp{id}_clubs' in st.session_state and len(st.session_state[f'grp{id}_clubs'])>0) else True) |
                                                            (pl.col('rider').is_in(st.session_state[f'grp{id}_riders']) if (f'grp{id}_riders' in st.session_state and len(st.session_state[f'grp{id}_riders'])>0) else False))['rider']

        grp_riders = st.multiselect('Rider(s)', 
                                    max_selections=10,
                                    key=f'grp{id}_riders', 
                                    options=grp_rider_choices,
                                    default=st.session_state[f'grp{id}_riders'] if (f'grp{id}_riders' in st.session_state) else None)

        grp_ids = [int(i.split(']')[0].split('[')[1]) for i in grp_riders]
    
    return grp_ids
"""