import os
import dash
import string
from dash.dependencies import Input, State, Output
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from pandas.tseries.offsets import *
import plotly.graph_objs as go
import numpy as np
from numpy import arange,array,ones
from scipy import stats
import psycopg2
from sqlalchemy import create_engine
from datetime import datetime
from collections import Counter
from flask import Flask, send_from_directory

app = dash.Dash(__name__)
server = app.server
app.title = 'Tweet MH'

@server.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(server.root_path, 'assets'), 'favicon.ico')

tweet_db_url = os.environ['DATABASE_URL']

def get_df_from_db(db_name):

    engine = create_engine(tweet_db_url)

    df = pd.read_sql_table(db_name, engine)

    df['TimeStamp'] = pd.to_datetime(df['TimeStamp'], unit='s')
    df = df.set_index(df['TimeStamp'])
    df = df[~df.index.duplicated(keep='first')].sort_index()

    df = df.loc[df.iloc[df.index.get_loc((df.index[-1] - pd.DateOffset(hours=1)), method='nearest')]['TimeStamp']:df.index[-1]]

    return df

def get_word_freq(df):
    # Set up to analyze
    text = ''
    for tweet in df['Tweets']:
        text += tweet + ' '

    text = text.translate(str.maketrans('','',string.punctuation))
    text = text.replace("’", "")
    freq_frame = map(str.lower, text.split())

    # Filter out for relevant words
    stop_words = [line.split() for line in open('stop_words.txt', 'r').readlines()]
    stop_words = [item for sublist in stop_words for item in sublist]

    freq_frame = [a for a in freq_frame if a not in stop_words]

    # Get most common occurrences in list of tweet words
    freq_frame = pd.DataFrame(Counter(freq_frame).most_common(5), columns=['Word','Occurs'])

    return freq_frame

def generate_table(dataframe, max_rows=10):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )


mhdf = get_df_from_db('mh_tweets')
midf = get_df_from_db('mi_tweets')
bddf = get_df_from_db('bd_tweets')
bhdf = get_df_from_db('bh_tweets')
mh_freq = get_word_freq(mhdf)
mi_freq = get_word_freq(midf)
bd_freq = get_word_freq(bddf)
bh_freq = get_word_freq(bhdf)
app.layout = html.Div(children=[
    html.Div(children=[
        html.H1(children='Tweet Mental Health Card'),
        html.Div(children=['''
            Hourly updated analyses on mental health related tweets
        ''',

            html.A(html.Button('Source Code!'),
                href='https://github.com/okstoic/tweetmh',
            ),
        ], className='description'),
    ], className='navigation'),

    html.Ul(children=[

      html.Li(children=[

            html.H1(children='Brain Health'),
            html.Div(children=[
                html.H2(children=['''Tweets''']),
                html.H1(children=[len(bhdf.index)]),
                html.H3(children=['''past hour'''])
            ], className = 'stat'),

            html.Div(children=[
                html.H2(children=['''Readability''']),
                html.H1(children=[np.round(bhdf["Readability"].mean(), decimals=2)]),
                html.H3(children=['''Flesch-Reading Scale'''])
            ], className = 'stat'),

            html.Div(children=[
                html.H2(children=['''Avg. Mood''']),
                html.H1(children=[np.round(bhdf["Polarity"].mean(), decimals=2)]),
                html.H3(children=['''TextBlob Sentiment Score'''])
            ], className = 'stat'),

            html.Div(children=[
                html.H2(children=['''Top Associations''']),
                generate_table(bh_freq),
            ], className = 'stat'),
        ], className = 'card'),

        html.Li(children=[

            html.H1(children='Mental Health'),
            html.Div(children=[
                html.H2(children=['''Tweets''']),
                html.H1(children=[len(mhdf.index)]),
                html.H3(children=['''past hour'''])
            ], className = 'stat'),

            html.Div(children=[
                html.H2(children=['''Readability''']),
                html.H1(children=[np.round(mhdf["Readability"].mean(), decimals=2)]),
                html.H3(children=['''Flesch-Reading Scale'''])
            ], className = 'stat'),

            html.Div(children=[
                html.H2(children=['''Avg. Mood''']),
                html.H1(children=[np.round(mhdf["Polarity"].mean(), decimals=2)]),
                html.H3(children=['''TextBlob Sentiment Score'''])
            ], className = 'stat'),

            html.Div(children=[
                html.H2(children=['''Top Associations''']),
                generate_table(mh_freq),
            ], className = 'stat'),
        ], className = 'card'),

        html.Li(children=[

            html.H1(children='Mental Illness'),
            html.Div(children=[
                html.H2(children=['''Tweets''']),
                html.H1(children=[len(midf.index)]),
                html.H3(children=['''past hour'''])
            ], className = 'stat'),

            html.Div(children=[
                html.H2(children=['''Readability''']),
                html.H1(children=[np.round(midf["Readability"].mean(), decimals=2)]),
                html.H3(children=['''Flesch-Reading Scale'''])
            ], className = 'stat'),

            html.Div(children=[
                html.H2(children=['''Avg. Mood''']),
                html.H1(children=[np.round(midf["Polarity"].mean(), decimals=2)]),
                html.H3(children=['''TextBlob Sentiment Score'''])
            ], className = 'stat'),

            html.Div(children=[
                html.H2(children=['''Top Associations''']),
                generate_table(mi_freq),
            ], className = 'stat'),
        ], className = 'card'),

      html.Li(children=[

            html.H1(children='Brain Disease'),
            html.Div(children=[
                html.H2(children=['''Tweets''']),
                html.H1(children=[len(bddf.index)]),
                html.H3(children=['''past hour'''])
            ], className = 'stat'),

            html.Div(children=[
                html.H2(children=['''Readability''']),
                html.H1(children=[np.round(bddf["Readability"].mean(), decimals=2)]),
                html.H3(children=['''Flesch-Reading Scale'''])
            ], className = 'stat'),

            html.Div(children=[
                html.H2(children=['''Avg. Mood''']),
                html.H1(children=[np.round(bddf["Polarity"].mean(), decimals=2)]),
                html.H3(children=['''TextBlob Sentiment Score'''])
            ], className = 'stat'),

            html.Div(children=[
                html.H2(children=['''Top Associations''']),
                generate_table(bd_freq),
            ], className = 'stat'),
        ], className = 'card'),

    ], className= 'card-layout')

])

if __name__ == '__main__':
    app.run_server(debug=True)
