import duckdb
from zrapp.endpoints import get_club_riders
from zrapp.helpers import unpack_riders

with open('data/clubs.txt', 'r') as file:
    clubs = file.read().split('\n')

data = get_club_riders(clubs)

df = unpack_riders(data)

with duckdb.connect('data/zrapp.duckdb') as con:
    con.sql('create schema if not exists core')
    con.sql('create or replace table core.riders as select * from df')