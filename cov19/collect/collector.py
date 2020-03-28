import json
import pandas as pd
import requests
from loguru import logger
from collections import OrderedDict
import cov19


class DataCollector:
    known_countries = {
        "Germany": "DE",
        "Austria": "AT",
        "Switzerland": "CH",
        "United Kingdom": "UK",
        "United States": "US"
    }

    def __init__(self, country):
        if country not in DataCollector.known_countries:
            raise ValueError("Unknown country. Please add a handler.")
        self.url = None
        self.data = OrderedDict()
        self.country = country
        self.data['country'] = DataCollector.known_countries[country]
        self.provinces = {}

    def get_cov19_data(self):
        return self.data

    def get_name(self):
        return self.country

    def check_data(self):
        if 'c' in self.data and 'd' in self.data:
            return True
        else:
            logger.error("Could not find numbers in web page for {}".format(self.country))
            return False

    def get_data_as_json(self):
        # if len==1 then the only element is data['country], i.e. there's no real data
        if len(self.data) == 1:
            return json.dumps({})
        else:
            return json.dumps(self.data)

    def _str2int(self, value) -> int:
        return int(str(value).replace(".", ""))


class Germany(DataCollector):
    def __init__(self):
        super().__init__("Germany")
        self.url = "https://www.rki.de/DE/Content/InfAZ/N/Neuartiges_Coronavirus/Fallzahlen.html"

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
                cases_title = tables[0].columns[1]
                cases = tables[0][cases_title][16]
                cases = int(cases)

                deaths_title = tables[0].columns[4]
                deaths = tables[0][deaths_title][16]
                deaths = int(deaths)

                self.data['c'] = cases
                self.data['d'] = deaths
            except ValueError:
                pass
            self.check_data()
        else:
            logger.error("Could not access statistics for Germany (status code={})".format(response.status_code))
        return self.get_data_as_json()
