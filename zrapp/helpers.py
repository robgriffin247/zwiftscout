import polars as pl
from datetime import datetime as dt
from datetime import timezone
import streamlit as st
import duckdb
from zrapp.endpoints import get_riders
from datetime import timedelta

def unpack_riders(data):

    if isinstance(data, dict):
        data = [data]

    riders = []

    for rider in data:
        if rider is not None:
            rider_keys = rider.keys()
            riders.append({
                
                'last_update': rider['last_update'],
                'rider_id': int(rider['riderId']) if 'riderId' in rider_keys else None,
                'name': str(rider['name']) if 'riderId' in rider_keys and 'name' in rider_keys else None,
                'rider': (f"[{str(rider['riderId'])}] {str(rider['name']).strip()}") if 'name' in rider_keys else None,
                'gender': str(rider['gender']) if 'gender' in rider_keys else None,
                'weight': float(rider['weight']) if 'weight' in rider_keys and float(rider['weight'])>0 else None,
                
                'club_id': int(rider['club']['id']) if 'club' in rider_keys and 'id' in rider['club'].keys() else None,
                'club': str(rider['club']['name']) if 'club' in rider_keys and 'name' in rider['club'].keys() else None,
            
                'watts_5': float(rider['power']['w5']) if 'power' in rider_keys and 'w5' in rider['power'].keys() and rider['power']['w5'] is not None else None,
                'watts_15': float(rider['power']['w15']) if 'power' in rider_keys and 'w15' in rider['power'].keys() and rider['power']['w15'] is not None else None,
                'watts_30': float(rider['power']['w30']) if 'power' in rider_keys and 'w30' in rider['power'].keys() and rider['power']['w30'] is not None else None,
                'watts_60': float(rider['power']['w60']) if 'power' in rider_keys and 'w60' in rider['power'].keys() and rider['power']['w60'] is not None else None,
                'watts_120': float(rider['power']['w120']) if 'power' in rider_keys and 'w120' in rider['power'].keys() and rider['power']['w120'] is not None else None,
                'watts_300': float(rider['power']['w300']) if 'power' in rider_keys and 'w300' in rider['power'].keys() and rider['power']['w300'] is not None else None,
                'watts_1200': float(rider['power']['w1200']) if 'power' in rider_keys and 'w1200' in rider['power'].keys() and rider['power']['w1200'] is not None else None,
                'watts_ftp': float(rider['zpFTP']) if 'zpFTP' in rider_keys and rider['zpFTP'] is not None else None,

                'wkg_5': float(rider['power']['wkg5']) if 'power' in rider_keys and 'wkg5' in rider['power'].keys() and rider['power']['wkg5'] is not None else None,
                'wkg_15': float(rider['power']['wkg15']) if 'power' in rider_keys and 'wkg15' in rider['power'].keys() and rider['power']['wkg15'] is not None else None,
                'wkg_30': float(rider['power']['wkg30']) if 'power' in rider_keys and 'wkg30' in rider['power'].keys() and rider['power']['wkg30'] is not None else None,
                'wkg_60': float(rider['power']['wkg60']) if 'power' in rider_keys and 'wkg60' in rider['power'].keys() and rider['power']['wkg60'] is not None else None,
                'wkg_120': float(rider['power']['wkg120']) if 'power' in rider_keys and 'wkg120' in rider['power'].keys() and rider['power']['wkg120'] is not None else None,
                'wkg_300': float(rider['power']['wkg300']) if 'power' in rider_keys and 'wkg300' in rider['power'].keys() and rider['power']['wkg300'] is not None else None,
                'wkg_1200': float(rider['power']['wkg1200']) if 'power' in rider_keys and 'wkg1200' in rider['power'].keys() and rider['power']['wkg1200'] is not None else None,
                'wkg_ftp': float(rider['zpFTP']) if 'zpFTP' in rider_keys and rider['zpFTP'] is not None else None,

                'velo': float(rider['race']['current']['rating']) if 'race' in rider_keys and 'current' in rider['race'].keys() and 'rating' in rider['race']['current'].keys() else None,
                'velo_category': str(rider['race']['current']['mixed']['category']) if 'race' in rider_keys and 'current' in rider['race'].keys() and 'mixed' in rider['race']['current'].keys() and 'category' in rider['race']['current']['mixed'].keys() else None,
                'velo_category_numeric': int(rider['race']['current']['mixed']['number']) if 'race' in rider_keys and 'current' in rider['race'].keys() and 'mixed' in rider['race']['current'].keys() and 'number' in rider['race']['current']['mixed'].keys() else None,
                'velo_30': float(rider['race']['max30']['rating']) if 'race' in rider_keys and 'max30' in rider['race'].keys() and 'rating' in rider['race']['current'].keys() else None,
                'velo_90': float(rider['race']['max90']['rating']) if 'race' in rider_keys and 'max90' in rider['race'].keys() and 'rating' in rider['race']['current'].keys() else None,
                
                'phenotype_sprinter': float(rider['phenotype']['scores']['sprinter']) if 'phenotype' in rider_keys and 'scores' in rider['phenotype'].keys() and 'sprinter' in rider['phenotype']['scores'].keys() else None,
                'phenotype_puncheur': float(rider['phenotype']['scores']['puncheur']) if 'phenotype' in rider_keys and 'scores' in rider['phenotype'].keys() and 'puncheur' in rider['phenotype']['scores'].keys() else None,
                'phenotype_pursuiter': float(rider['phenotype']['scores']['pursuiter']) if 'phenotype' in rider_keys and 'scores' in rider['phenotype'].keys() and 'pursuiter' in rider['phenotype']['scores'].keys() else None,
                'phenotype_climber': float(rider['phenotype']['scores']['climber']) if 'phenotype' in rider_keys and 'scores' in rider['phenotype'].keys() and 'climber' in rider['phenotype']['scores'].keys() else None,
                'phenotype_tt': float(rider['phenotype']['scores']['tt']) if 'phenotype' in rider_keys and 'scores' in rider['phenotype'].keys() and 'tt' in rider['phenotype']['scores'].keys() else None,
                'phenotype_value': str(rider['phenotype']['value']) if 'phenotype' in rider_keys and 'value' in rider['phenotype'].keys() else None,
            
                })


    df = pl.DataFrame(riders)

    return df 


def update_selected_riders(grp1, grp2):

    selected_riders = st.session_state['df_riders'].filter(pl.col('rider_id').is_in(grp1 + grp2))
    stale_riders = selected_riders.filter((pl.col('last_update')<dt.now()-timedelta(days=3)))['rider_id'].unique().to_list()

    if len(stale_riders)>0:
        updated_riders = unpack_riders(get_riders(stale_riders))
        st.session_state['df_riders'] = pl.concat([
            st.session_state['df_riders'],
            updated_riders,
            ]).sort(['rider_id', 'last_update'])
        
    st.session_state['df_riders'] = st.session_state['df_riders'].unique(subset='rider_id', keep='last')
         
    with duckdb.connect('data/zrapp.duckdb') as con:
        data = st.session_state['df_riders']
        con.sql('create or replace table core.riders as select * from data')

