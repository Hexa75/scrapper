import streamlit as st
from src.control.control import Control
import altair as alt
import pandas as pd
from datetime import datetime




class View:

    def __init__(self):
        st.title('Analyse des revues sur Trustpilot')

        with st.sidebar:
            st.caption('mockup by Hexamind.ai')
            company = st.text_input('Société', 'leocare')
            max_pages = st.number_input('nombre de pages max à explorer', 1)

        data_load_state = st.text('Loading data...')
        st.spinner("loading...")

        df, results = Control(company, max_pages).run()

        df['ratings'] = df['ratings'].astype(int) - 3
        df['dates'] = pd.to_datetime(df['dates'])
        df['reviews'] = df['reviews'].astype(str)
        df['size'] = 2

        all_symbols = ['très mauvais', 'mauvais', 'partagé', 'bon', 'très bon']

        symbols = st.multiselect("Choose ratings to visualize", all_symbols, all_symbols)

 #       source = source[source.symbol.isin(symbols)]

        chart = alt.Chart(df).mark_circle()\
            .encode(x='dates', y='ratings', color='ratings:N', tooltip=['reviews'])\
            .properties(width=1000, height=500)

        st.altair_chart(chart, use_container_width=True)

        data_load_state.text('Loading data...done!')
        st.subheader('Les revues pour '+company)
        st.write(results)
        st.write(df)
