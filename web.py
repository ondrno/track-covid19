import os
import json
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import flask
import pandas as pd
from datetime import datetime
from flask_caching import Cache
from loguru import logger
from cov19 import Cov19Statistics, get_query_interval
from cov19.collect import Austria, Germany, Switzerland, UnitedKingdom, UnitedStates


external_stylesheets = [
    # Dash CSS
    'https://codepen.io/chriddyp/pen/bWLwgP.css',
    # Loading screen CSS
    'https://codepen.io/chriddyp/pen/brPBPO.css']

server = flask.Flask(__name__)
app = dash.Dash(__name__, server=server, external_stylesheets=external_stylesheets)
app.config.suppress_callback_exceptions = True

CACHE_CONFIG = {
    'CACHE_TYPE': 'filesystem',
    'CACHE_DIR': os.environ.get('CACHE_DIR', 'cache-directory')
}
cache = Cache()
cache.init_app(server, config=CACHE_CONFIG)


@app.callback(Output('signal', 'children'), [Input('interval-component', 'n_intervals')])
def collect_data(n):
    # get data from web sites and send a signal when done
    global_store()


@cache.memoize(timeout=os.environ.get('CACHE_TIMEOUT', 120))
def global_store():
    # perform expensive computations in this "global store"
    # these computations are cached in a globally available
    # redis memory store which is available across processes
    # and for all time.
    # do the real job, i.e. 1) get data from web site, 2) store it into a file and 3) then read the data into data frame
    cov19 = Cov19Statistics()
    for country in [Germany, Austria, Switzerland, UnitedKingdom, UnitedStates]:
        c = country()
        cov19.add_country(c)

    cov19.write_statistics_to_file()
    groups = read_data_as_groups(cov19.log_file)
    de = groups.get_group('DE')
    at = groups.get_group('AT')
    ch = groups.get_group('CH')
    uk = groups.get_group('UK')
    us = groups.get_group('US')
    return de, at, ch, uk, us


def serve_layout():
    return html.Div(children=[
        # hidden signal value
        html.Div(id='signal', style={'display': 'none'}),

        dcc.Interval(
            id='interval-component',
            interval=get_query_interval(),
            n_intervals=0
        ),
        html.H1(children='Covid-19 Statistics (D, A, CH, UK, US)'),

        html.Div(children=[
            'Sources: ',
            dcc.Link('Robert-Koch-Institut (DE)',
                     href='https://www.rki.de/DE/Content/InfAZ/N/Neuartiges_Coronavirus/Fallzahlen.html'),
            ', ',
            dcc.Link('Sozialministerium (AT)',
                     href='https://www.sozialministerium.at/Informationen-zum-Coronavirus/Neuartiges-Coronavirus-(2019-nCov).html'),
            ', ',
            dcc.Link('Bundesamt fuer Gesundheit (CH)',
                     href='https://www.bag.admin.ch/bag/de/home/krankheiten/ausbrueche-epidemien-pandemien/aktuelle-ausbrueche-epidemien/novel-cov/situation-schweiz-und-international.html'),
            ', ',
            dcc.Link('British Governement (UK)',
                     href='https://www.arcgis.com/sharing/rest/content/items/bc8ee90225644ef7a6f4dd1b13ea1d67/data'),
            ', ',
            dcc.Link('Centers for Disease Control and Prevention (US)',
                     href='https://www.cdc.gov/coronavirus/2019-ncov/cases-updates/cases-in-us.html?CDC_AA_refVal=https%3A%2F%2Fwww.cdc.gov%2Fcoronavirus%2F2019-ncov%2Fcases-in-us.html'),
            html.Br(),
            html.Div(id='last-updated')
        ]),
        dcc.Graph(id='covid-cases-graph'),
        dcc.Graph(id='covid-deaths-graph'),
    ])


def read_data_as_groups(logfile):
    with open(logfile) as f:
        data = []
        for line in f.readlines():
            data.append(json.loads(line))
        df = pd.json_normalize(data)
    df.drop_duplicates(keep='last', subset=['country', 'c', 'd'], inplace=True)
    groups = df.groupby('country')
    return groups


@app.callback(Output('last-updated', 'children'), [Input('signal', 'children')])
def update_metrics_text(n):
    today = datetime.now().isoformat()
    style = {'fontSize': '11px'}
    return [
        html.Span('Last update: {}'.format(today), style=style)
    ]


@app.callback(Output('covid-cases-graph', 'figure'), [Input('signal', 'children')])
def update_covid_cases_metrics(n):
    de, at, ch, uk, us = global_store()
    fig = {
        'data': [
            {'x': at["date"], 'y': at["c"], 'name': "Austria"},
            {'x': de["date"], 'y': de["c"], 'name': "Germany"},
            {'x': ch["date"], 'y': ch["c"], 'name': "Switzerland"},
            {'x': uk["date"], 'y': uk["c"], 'name': "United Kingdom"},
            {'x': us["date"], 'y': us["c"], 'name': "United States"},
        ],
        'layout': {
            'title': 'Confirmed cases'
        }
    }
    return fig


@app.callback(Output('covid-deaths-graph', 'figure'), [Input('signal', 'children')])
def update_covid_deaths_metrics(n):
    de, at, ch, uk, us = global_store()
    fig = {
        'data': [
            {'x': at["date"], 'y': at["d"], 'name': "Austria"},
            {'x': de["date"], 'y': de["d"], 'name': "Germany"},
            {'x': ch["date"], 'y': ch["d"], 'name': "Switzerland"},
            {'x': uk["date"], 'y': uk["d"], 'name': "United Kingdom"},
            {'x': us["date"], 'y': us["d"], 'name': "United States"},
        ],
        'layout': {
            'title': 'Confirmed deaths'
        }
    }
    return fig


app.layout = serve_layout


if __name__ == '__main__':
    logger.info("Update cycle={} minutes", get_query_interval() / 1000 / 60)
    app.run_server(port=os.environ.get('PORT', 8050))
