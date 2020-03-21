import dash
import dash_core_components as dcc
import dash_html_components as html
import flask
import pandas as pd
from datetime import datetime as dt
from datetime import timedelta


def normalize_data(df: pd.DataFrame):
    # c.f. https://skipperkongen.dk/2018/11/26/how-to-fill-missing-dates-in-pandas/
    full_index = pd.date_range(start=df.ts.min(), end=df.ts.max())
    df.set_index('ts').reindex(full_index).fillna(0.0).rename_axis('ts').reset_index()
    return df


def convert_data(infile: str = "../log/cov19_statistics.log"):
    df = pd.read_csv(infile, sep=";")
    df['dt'] = df.apply(lambda row: dt(row["year"], row["month"], row["day"], row['hour'], row['minute']).isoformat(), axis=1)
    del df['year']
    del df['month']
    del df['day']
    del df['hour']
    del df['minute']
    df = df[['dt', 'country', 'cases', 'death', 'recovered']]
    df.to_csv('cov19_stats.log', index=False, sep=";")


def read_data(logfile: str = "../log/cov19_statistics.log"):
    df = pd.read_csv(logfile, sep=";")
    # df['ts'] = df.apply(lambda x: pd.to_datetime("{}-{}-{}T{}:{}".format(x['year'], x['month'], x['day'], x['hour'], x['minute'])), axis=1)

    # df.drop_duplicates(keep='last', subset=['dt', 'country'], inplace=True)

    # de = df[df['country'] == "DE"]
    # full_index = pd.date_range(start=de.dt.min(), end=de.dt.max(), freq='D')
    # bar = de.set_index('dt')
    # foo = de.reindex(full_index)
    # foobar = bar.reindex(full_index)
    #
    # de_normalized = normalize_data(de)

    grouped = df.groupby('country')
    de = grouped.get_group('DE')
    at = grouped.get_group('AT')
    ch = grouped.get_group('CH')
    uk = grouped.get_group('UK')
    us = grouped.get_group('US')

    # df['new_cases'] = df.apply(lambda x: x.datetime.shift(1) - x.cases.shift(1), axis=1)
    # df['grow_rate'] = df.apply(lambda x: x.cases.shift(1)/x.cases, axis=1)
    # de = df[df['country'] == "DE"]
    # today = dt.today()
    # yesterday = dt(2020, 3, 16) - timedelta(days=1)
    # # yesterday = dt(today.year, today.month, today.day) - timedelta(days=1)
    # df['grow_rate'] = df.apply(lambda x: calc_grow_rate(x.cases, ), axis=1)

    # at = df[df['country'] == "AT"]
    # ch = df[df['country'] == "CH"]
    # uk = df[df['country'] == "UK"]
    # us = df[df['country'] == "US"]

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
        ),

        dcc.Graph(
            id='covid-deaths',
            figure={
                'data': [
                    {'x': at["dt"], 'y': at["death"], 'name': "Austria"},
                    {'x': de["dt"], 'y': de["death"], 'name': "Germany"},
                    {'x': ch["dt"], 'y': ch["death"], 'name': "Switzerland"},
                    {'x': uk["dt"], 'y': uk["death"], 'name': "United Kingdom"},
                    {'x': us["dt"], 'y': us["death"], 'name': "United States"},
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
    # convert_data()
    df = read_data()
    app.run_server(port=8050)
