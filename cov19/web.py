import dash
import dash_core_components as dcc
import dash_html_components as html
import flask
import pandas as pd
from datetime import datetime as dt


def read_data(logfile: str = "../log/cov19_statistics.log"):
    df = pd.read_csv(logfile, sep=";")

    df['datetime'] = df.apply(lambda row: dt(row["year"], row["month"], row["day"]), axis=1)
    df.drop_duplicates(keep='last', subset=['datetime', 'country'], inplace=True)

    # df['new_cases'] = df.apply(lambda x: x.datetime.shift(1) - x.cases.shift(1), axis=1)
    # df['grow_rate'] = df.apply(lambda x: x.cases.shift(1)/x.cases, axis=1)
    de = df[df['country'] == "DE"]
    at = df[df['country'] == "AT"]
    ch = df[df['country'] == "CH"]
    uk = df[df['country'] == "UK"]
    us = df[df['country'] == "US"]

    return de, at, ch, uk, us


def serve_layout():
    de, at, ch, uk, us = read_data()
    return html.Div(children=[
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
        ]),

        dcc.Graph(
            id='covid-cases',
            figure={
                'data': [
                    {'x': at["datetime"], 'y': at["cases"], 'name': "Austria"},
                    {'x': de["datetime"], 'y': de["cases"], 'name': "Germany"},
                    {'x': ch["datetime"], 'y': ch["cases"], 'name': "Switzerland"},
                    {'x': uk["datetime"], 'y': uk["cases"], 'name': "United Kingdom"},
                    {'x': us["datetime"], 'y': us["cases"], 'name': "United States"},
                ],
                'layout': {
                    'title': 'Confirmed cases'
                }
            }
        ),

        dcc.Graph(
            id='covid-deaths',
            figure={
                'data': [
                    {'x': at["datetime"], 'y': at["death"], 'name': "Austria"},
                    {'x': de["datetime"], 'y': de["death"], 'name': "Germany"},
                    {'x': ch["datetime"], 'y': ch["death"], 'name': "Switzerland"},
                    {'x': uk["datetime"], 'y': uk["death"], 'name': "United Kingdom"},
                    {'x': us["datetime"], 'y': us["death"], 'name': "United States"},
                ],
                'layout': {
                    'title': 'Confirmed deaths'
                }
            }
        )
    ])


server = flask.Flask(__name__)
app = dash.Dash(__name__, server=server)
app.config.suppress_callback_exceptions = True

app.layout = serve_layout

if __name__ == '__main__':
    df = read_data()
    app.run_server(port=8050)
