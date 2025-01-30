import streamlit as st
from openai import OpenAI
from zrapp.endpoints import get_riders


col1, col2 = st.columns([7,3])

with col1:
    route = st.text_input('Route', 
                          placeholder='Enter Zwift route name, e.g. "whole lotta lava"',
                          help='This data is read by OpenAI so it doesn\'t need to be spelled or formatted perfectly; it will cope with "Road To Sky, Watopia" just as well as it will "ROAD TO SKY", or "Road to sky" or WatoPIa RoAd tO SKY"' )

with col2:
    laps = st.number_input('Laps', value=1, min_value=1, max_value=25)

notes = st.text_area('Additional Notes')

if st.button('Get Tactics!'):
    st.toast('On the team radio with the directeur sportif, please wait...')

    client = OpenAI(
    api_key=st.secrets['openai_api']['key'])

    st.toast('Filling bidons...')

    completion = client.chat.completions.create(
    model='gpt-4o-mini',
    store=True,
    messages=[
        {'role': 'user', 
        'content': f'''
        I am preparing for a Zwift cycling race.
        The race involves two teams of up to five riders per team.
        The race format means points are awared as 10 for first place, 9 for second continuing to 1pt for 10th.
        The team with the most points wins.
        The race covers {laps} laps of the {route} route.
        Rider data is given in python lists of dictionaries, one dictionary per rider, one list per team.
        The variables in power w<seconds> and wkg<second> give the riders peak power over the given number of seconds - short durations good for sprinting, long good for solo efforts and climbings.
        The varables under phenotype-score give scores from 0 to 100 scoring the riders ability as a sprinter, puncheur, pursuiter, climber and timetrialist.
        The variables under "race" current, max30 and max90 give current, 30 day peak and 90 day peak velo scores (rating) - velo is a scoring system similar to ELO in chess, ranging from 0 (bad) to 3000 (good) and affected by racing results. 
        The riders in team one are {get_riders([3113376, 5083506, 5639087, 5859202, 5879996], toast=False)}.
        The riders in team two are {get_riders([448756, 817572, 2419188, 4658834, 5583190], toast=False)}.
        Considering the profile of the route, race points format, and strengths and weaknesses of each team and rider,
        generate three strategies for team one to win the race, highlighting where and how to attack and 
        the roles of each rider through the race.
        
        First provide a very concise summary of the route (<=100 words), including start and end of significant climbs and tactically important areas.
        Then provide the three suggested strategies, keeping it concise (<120 words each) and in bulletpoints if appropriate.
        Finally provide a concise (<150 word) summary of what to be wary of with the other team, highlighting how they might approach the race and how to counteract that.
        
        Also consider user feedback which may include details such as how riders are feeling, notes on current or recent form, preferred or suggested tactics or details on the route.
        The user passed this information:
        
        {notes}
        '''
        }
    ]
    )

    st.toast('Fetching gels...')

    message = completion.choices[0].message.content

    st.write(message)