import streamlit as st
from ui.coffee import buy_coffee

st.markdown('''
ZwiftScout is designed to provide a platform for racers to compare racers &mdash; 
perfect when you want to develop a race strategy or select riders for your team!
            
It was designed with the Club Ladder racing series in mind (but is useful in any race), 
making it easy to get and compare data for riders split into two teams, visualising 
racer power data and phenotypes.
         
Data comes from the ZwiftRacing.app &mdash; thanks to Tim Hanson for not just creating ZRapp,
but also providing an API which provides access to the data.
         
*Ride on!*
                     
------
         
ZwiftScout is created by Rob Griffin, a Data/Analytics Engineer and keen Zwifter, racing for Tea & Scone.
Check out his GitHub for a [demo of the ZwiftRacing.app API](https://github.com/robgriffin247/zrapp_demo) and other projects.

------
            
*Updated 2025-01-29*
            
------
''')

buy_coffee()