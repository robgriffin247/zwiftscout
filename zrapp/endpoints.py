import httpx
import streamlit as st
from datetime import datetime as dt
import json


def get_riders(ids, toast=True):
    
    if isinstance(ids, int):
        ids = [ids]
    
    header = {'Authorization':st.secrets['zrapp_api']['key']}
    url = f'https://zwift-ranking.herokuapp.com/public/riders/'

    response = httpx.post(url,
                          headers=header, 
                          json=ids, 
                          timeout=30)
    response.raise_for_status()

    content = response.content
    decoded = content.decode(encoding='utf-8')
    riders = json.loads(decoded)

    for rider in riders:
        rider['last_update'] = dt.now()

    if toast and len(ids)==1:
        st.toast('Added rider!')
    elif toast and len(ids)>1:
        st.toast(f'Added {len(ids)} riders!')
    else:
        pass

    return riders


def get_club_riders(ids, toast=True):

    if isinstance(ids, int):
        ids = [ids]


    def get_club(id):
        header = {'Authorization':st.secrets['zrapp_api']['key']}
        url = f'https://zwift-ranking.herokuapp.com/public/clubs/{id}'

        response = httpx.get(url, headers=header, timeout=30)
        response.raise_for_status()

        return {'club':response.json(), 'date':dt.now()}#response.headers['date']}


    def get_club_from_rider(club, rider):
        header = {'Authorization':st.secrets['zrapp_api']['key']}
        url = f'https://zwift-ranking.herokuapp.com/public/clubs/{club}/{rider}'

        response = httpx.get(url, headers=header, timeout=30)
        response.raise_for_status()

        return {'club':response.json(), 'date':dt.now()}#response.headers['date']}
    
    riders = []

    i = 0
    
    if toast:
        msg = st.toast('Loading Riders...')

    for id in ids:
    
        i += 1
        data = get_club(id)
        club_riders = data['club']['riders']

        page_length = len(club_riders)
        while page_length==1000:
            next_riders = get_club_from_rider(id, 1 + club_riders[-1]['riderId'])['club']['riders']
            page_length = len(next_riders)
            for rider in next_riders:
                club_riders.append(rider)
        
        for rider in club_riders:
            rider['club'] = {'id':data['club']['clubId'], 'name': data['club']['name']}
            rider['last_update'] = data['date']
            riders.append(rider)

        if toast:
            msg = st.empty()
            msg.toast(f'Loaded {i} of {len(ids)} clubs - {len(riders)} riders loaded!')
        else:
            print(f'Loaded {i} of {len(ids)} clubs - {len(riders)} riders loaded!')

    return riders
