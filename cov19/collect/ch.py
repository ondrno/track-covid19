import requests
import re
from bs4 import BeautifulSoup
import pandas as pd
from cov19.collect import DataCollector


class Switzerland(DataCollector):
    def __init__(self):
        super().__init__("Switzerland")
        self.url = "https://www.bag.admin.ch/bag/de/home/krankheiten/ausbrueche-epidemien-pandemien/aktuelle-ausbrueche-epidemien/novel-cov/situation-schweiz-und-international.html"

    def get_cov19_data(self):
        response = requests.get(self.url)
        tables = pd.read_html(response.text)
        self.get_total_cases(tables[0])
        self.get_total_deaths(tables[0])

        self.check_data()
        return self.get_data_as_json()

    def get_total_cases(self, table):
        raw_cases = table['Total seit Beginn der Epidemie'][0]
        cases = int(raw_cases.replace(" ", ""))
        self.data['c'] = cases

    def get_total_deaths(self, table):
        raw_deaths = table['Total seit Beginn der Epidemie'][2]
        deaths = int(raw_deaths.replace(" ", ""))
        deaths = int(deaths)
        self.data['d'] = deaths
