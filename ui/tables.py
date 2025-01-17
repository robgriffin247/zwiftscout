import streamlit as st

def rider_table(selected_riders_data):
    
    st.html('</br>')

    table_cont = st.container()

    wkg = st.toggle('W/kg', value=False, key='rider_table_wkg_toggle')

    if wkg:
        source = selected_riders_data[['grp', 'name', 'velo', 'phenotype_value',
                                       'weight', 'wkg_5', 'wkg_60', 'wkg_300', 'wkg_ftp',]]
    else:
        source = selected_riders_data[['grp', 'name', 'velo', 'phenotype_value',
                                       'weight', 'watts_5', 'watts_60', 'watts_300', 'watts_ftp',]]

    table_cont.dataframe(source,
                 use_container_width=True,
        column_config={
            'grp':st.column_config.TextColumn('Team'),
            'name':st.column_config.TextColumn('Rider'),
            'weight':st.column_config.NumberColumn('kg', format='%.1f'),
            'phenotype_value':st.column_config.TextColumn('Phenotype'),
            'velo':st.column_config.NumberColumn('vELO', format='%.0f'),
            'velo_90':st.column_config.NumberColumn('vELO (90)', format='%.0f'),
            'watts_5':st.column_config.NumberColumn('5s Power', format='%.0f'),
            'wkg_5':st.column_config.NumberColumn('5s Power', format='%.2f'),
            'watts_60':st.column_config.NumberColumn('1m Power', format='%.0f'),
            'wkg_60':st.column_config.NumberColumn('1m Power', format='%.2f'),
            'watts_300':st.column_config.NumberColumn('5m Power', format='%.0f'),
            'wkg_300':st.column_config.NumberColumn('5m Power', format='%.2f'),
            'watts_ftp':st.column_config.NumberColumn('FTP', format='%.0f'),
            'wkg_ftp':st.column_config.NumberColumn('FTP', format='%.2f'),
        }
    )