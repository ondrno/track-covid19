import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import flask
import pandas as pd
from datetime import datetime


server = flask.Flask(__name__)
app = dash.Dash(__name__, server=server)
app.config.suppress_callback_exceptions = True


def serve_layout():
    # two_hours_in_ms = 2 * 3600 * 1000
    two_hours_in_ms = 60 * 1000
    return html.Div(children=[
        dcc.Interval(
            id='interval-component',
            interval=two_hours_in_ms,
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


def read_data(logfile: str = "../log/cov19_statistics.log"):
    df = pd.read_csv(logfile, sep=";")
    df.drop_duplicates(keep='last', subset=['country', 'cases', 'deaths', 'recovered'], inplace=True)
    grouped = df.groupby('country')
    de = grouped.get_group('DE')
    at = grouped.get_group('AT')
    ch = grouped.get_group('CH')
    uk = grouped.get_group('UK')
    us = grouped.get_group('US')
    return de, at, ch, uk, us


@app.callback(Output('last-updated', 'children'),
              [Input('interval-component', 'n_intervals')])
def update_metrics_text(n):
    today = datetime.now().isoformat()
    style = {'fontSize': '11px'}
    return [
        html.Span('Last update: {}'.format(today), style=style)
    ]


@app.callback(Output('covid-cases-graph', 'figure'),
              [Input('interval-component', 'n_intervals')])
def update_covid_cases_metrics(n):
    de, at, ch, uk, us = read_data()
    fig={
        'data': [
            {'x': at["dt"], 'y': at["cases"], 'name': "Austria"},
            {'x': de["dt"], 'y': de["cases"], 'name': "Germany"},
            {'x': ch["dt"], 'y': ch["cases"], 'name': "Switzerland"},
            {'x': uk["dt"], 'y': uk["cases"], 'name': "United Kingdom"},
            {'x': us["dt"], 'y': us["cases"], 'name': "United States"},
        ],
        'layout': {
            'title': 'Confirmed cases'
        }
    }
    return fig


@app.callback(Output('covid-deaths-graph', 'figure'),
              [Input('interval-component', 'n_intervals')])
def update_covid_cases_metrics(n):
    de, at, ch, uk, us = read_data()
    fig = {
        'data': [
            {'x': at["dt"], 'y': at["deaths"], 'name': "Austria"},
            {'x': de["dt"], 'y': de["deaths"], 'name': "Germany"},
            {'x': ch["dt"], 'y': ch["deaths"], 'name': "Switzerland"},
            {'x': uk["dt"], 'y': uk["deaths"], 'name': "United Kingdom"},
            {'x': us["dt"], 'y': us["deaths"], 'name': "United States"},
        ],
        'layout': {
            'title': 'Confirmed deaths'
        }
    }
    return fig

app.layout = serve_layout


if __name__ == '__main__':
    # df = read_data()
    app.run_server(port=8050)
