import streamlit as st
import plotly.express as px
import plotly.graph_objs as go
import polars as pl
import math

def phenotypes_plot(selected_riders_data):

    fig_cont = st.container()
    
    team_view = st.toggle('Show Team Averages', value=True, key='team_view_pheno')
    
    source = selected_riders_data[['name', 'grp', 'rider_id', 'phenotype_sprinter', 
                                 'phenotype_puncheur', 'phenotype_pursuiter', 
                                 'phenotype_climber', 'phenotype_tt']]

    rotated = source.unpivot(index=['rider_id', 'name', 'grp'])


    fig = px.line(rotated, 
                  x='variable', y='value', color='name', line_dash='grp',
                  markers=True, labels={'name':'Rider', 'grp':'Selected Team'})
    
    fig.layout.legend.title.text='Rider'
    
    for i in range(0,selected_riders_data.shape[0]):
        fig.data[i].name = fig.data[i].name[0:-3]
    if team_view:
        fig.layout.legend.title.text='Team'
        rotated_grp = source.drop(['rider_id', 'name']).group_by('grp').mean().unpivot(index=['grp'])
        fig.update_traces(line=dict(color='rgba(150, 150, 150, 0.5)', width=0.5))
        fig.update_layout(showlegend=False)
        fig.add_traces(px.line(rotated_grp,
                               x='variable', y='value', line_dash='grp', color='grp',
                               markers=True, labels={'grp':'Selected Team'}).data)
    

    fig.update_layout(xaxis_title=None, yaxis_title=None,
                      legend={'orientation':'h', 'yanchor':'top', 'xanchor':'left', 'x':0, 'y':-0.16})

    fig.update_xaxes(
        tickvals=[0,1,2,3,4],
        ticktext=['Sprinter', 'Puncheur', 'Pursuiter', 'Climber', 'Time-Trialist']
        )

    fig_cont.plotly_chart(fig)

    return fig


def power_curves_plot(selected_riders_data):
    
    fig_cont = st.container()

    col1, col2, _= st.columns([5,4,8])
    with col1:
        team_view = st.toggle('Show Team Averages', value=True, key='team_view_power')
    with col2:
        wkg = st.toggle('W/kg', value=False, key='power_curve_wkg_toggle')

    if wkg:
        source = selected_riders_data[['grp', 'name', 'rider_id', 
                                       'wkg_5', 'wkg_15', 'wkg_30', 'wkg_60', 'wkg_120', 'wkg_300', 'wkg_1200',]]
        title_suffix = ' (W/kg)'
    else:
        source = selected_riders_data[['grp', 'name', 'rider_id',
                                       'watts_5', 'watts_15', 'watts_30', 'watts_60', 'watts_120', 'watts_300', 'watts_1200',]]
        title_suffix = ' (Watts)'


    rotated = source.unpivot(index=['rider_id', 'name', 'grp'])

    rotated = rotated.with_columns(pl.col('variable').str.split_exact('_', 1).struct.rename_fields(['_', 'time']).alias('fields')).unnest('fields')

    rotated = rotated.with_columns(log_time=pl.col('time').log(base=2))



    fig = px.line(rotated, title=f'Power Curves{title_suffix}', x='log_time', y='value', color='name', line_dash='grp', markers=True,
                  labels={
                      'name':'Rider',
                      'grp':'Selected Team'
                  })


    fig = px.line(rotated, 
                  x='log_time', y='value', color='name', line_dash='grp',
                  markers=True, labels={'name':'Rider', 'grp':'Selected Team'})
    
    fig.layout.legend.title.text='Rider'
    
    for i in range(0,selected_riders_data.shape[0]):
        fig.data[i].name = fig.data[i].name[0:-3]
    if team_view:
        fig.layout.legend.title.text='Team'
        rotated_grp = source.drop(['rider_id', 'name']).group_by('grp').mean().unpivot(index=['grp'])
        rotated_grp = rotated_grp.with_columns(pl.col('variable').str.split_exact('_', 1).struct.rename_fields(['_', 'time']).alias('fields')).unnest('fields')
        rotated_grp = rotated_grp.with_columns(log_time=pl.col('time').log(base=2))

        fig.update_traces(line=dict(color='rgba(150, 150, 150, 0.5)', width=0.5))
        fig.update_layout(showlegend=False)

        fig.add_traces(px.line(rotated_grp,
                               x='log_time', y='value', line_dash='grp', color='grp',
                               markers=True, labels={'grp':'Selected Team'}).data)
    



    fig.update_layout(xaxis_title=None, yaxis_title=None,
                      legend={'orientation':'h', 'yanchor':'top', 'xanchor':'left', 'x':0, 'y':-0.16})

    fig.update_xaxes(
        tickvals=[math.log2(i) for i in [5,15,30,60,120,300,1200]],
        ticktext=['5s', '15s', '30s', '1min', '2min', '5min', '20min']
        )

    fig_cont.plotly_chart(fig)

    return fig

