import pandas as pd
import requests
from loguru import logger
from collections import OrderedDict
import cov19
from cov19.collect import DataCollector


class Germany(DataCollector):
    provinces = {
        "Baden-Würtemberg": {"short_name": "BW", "pos": 0},
        "Bayern": {"short_name": "BY", "pos": 1},
        "Berlin": {"short_name": "BE", "pos": 2},
        "Brandenburg": {"short_name": "BB", "pos": 3},
        "Bremen": {"short_name": "HB", "pos": 4},
        "Hamburg": {"short_name": "HH", "pos": 5},
        "Hessen": {"short_name": "HE", "pos": 6},
        "Mecklenburg-Vorpommern": {"short_name": "MV", "pos": 7},
        "Niedersachsen": {"short_name": "NI", "pos": 8},
        "Nordrhein-Westfalen": {"short_name": "NW", "pos": 9},
        "Rheinland-Pfalz": {"short_name": "RP", "pos": 10},
        "Saarland": {"short_name": "SL", "pos": 11},
        "Sachsen": {"short_name": "SN", "pos": 12},
        "Sachsen-Anhalt": {"short_name": "ST", "pos": 13},
        "Schleswig-Holstein": {"short_name": "SH", "pos": 14},
        "Thüringen": {"short_name": "TH", "pos": 15},
    }

    def __init__(self):
        super().__init__("Germany")
        self.provinces = Germany.provinces
        self.url = "https://www.rki.de/DE/Content/InfAZ/N/Neuartiges_Coronavirus/Fallzahlen.html"
        self.cases_col = 1
        self.deaths_col = 5

    def get_cov19_data(self) -> OrderedDict:
        try:
            response = requests.get(self.url)
        except (requests.exceptions.HTTPError,
                requests.exceptions.ConnectionError,
                requests.exceptions.Timeout):
            raise cov19.exceptions.RequestError(self.url)
        if response.status_code == 200:
            try:
                tables = pd.read_html(response.text, thousands=".", decimal=";")
                self.get_total_cases(tables[0])
                self.get_total_deaths(tables[0])

                self.get_data_by_province(tables[0])

            except ValueError:
                pass
            self.check_data()
        else:
            logger.error("Could not access statistics for Germany (status code={})".format(response.status_code))
        return self.get_data_as_json()

    def get_total_cases(self, table):
        cases_title = table.columns[self.cases_col]
        cases = table[cases_title][16]
        cases = int(cases)
        self.data['c'] = cases

    def get_total_deaths(self, table):
        deaths_title = table.columns[self.deaths_col]
        deaths = table[deaths_title][16]
        deaths = int(deaths)
        self.data['d'] = deaths

    def get_data_by_province(self, table):
        cases_title = table.columns[self.cases_col]
        deaths_title = table.columns[self.deaths_col]
        if not self.data.get('provinces'):
            self.data['provinces'] = OrderedDict()
        for province in self.provinces.keys():
            short_name = self.provinces[province]["short_name"]
            pos = self.provinces[province]["pos"]
            if not self.data['provinces'].get(short_name):
                self.data['provinces'][short_name] = OrderedDict()

            cases = table[cases_title][pos]
            cases = int(cases)
            self.data['provinces'][short_name]['c'] = cases

            deaths = table[deaths_title][pos]
            try:
                deaths = int(deaths)
            except ValueError:
                deaths = 0
            self.data['provinces'][short_name]['d'] = deaths
