import pandas as pd
import requests
from loguru import logger
import cov19
from cov19.collect import DataCollector


class UnitedKingdom(DataCollector):
    def __init__(self):
        super().__init__("United Kingdom")
        self.url = "https://www.gov.uk/guidance/coronavirus-covid-19-information-for-the-public"

    def get_cov19_data(self):
        try:
            response = requests.get(self.url)
        except (requests.exceptions.HTTPError,
                requests.exceptions.ConnectionError,
                requests.exceptions.Timeout):
            raise cov19.exceptions.RequestError(self.url)
        if response.status_code == 200:
            try:
                tables = pd.read_html(response.text, thousands=",", decimal=";")
                self.get_total_cases(tables[0])
                self.get_total_deaths(tables[0])
            except ValueError:
                pass
        else:
            logger.error("Could not access statistics for United Kingdom (status code={})".format(response.status_code))
        self.check_data()
        return self.get_data_as_json()

    def get_total_cases(self, table):
        cases = table['Number of positive cases'][1]
        cases = int(cases)
        self.data['c'] = cases

    def get_total_deaths(self, table):
        deaths = table['Deaths in all settings'][1]
        deaths = int(deaths)
        self.data['d'] = deaths
