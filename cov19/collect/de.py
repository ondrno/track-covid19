import pandas as pd
import requests
from loguru import logger
from collections import OrderedDict
import cov19
from cov19.collect import DataCollector


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
