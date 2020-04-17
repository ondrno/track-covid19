import requests
import re
import pandas as pd
from bs4 import BeautifulSoup
from collections import OrderedDict
from cov19.collect import DataCollector


class Austria(DataCollector):
    provinces = {
        'Burgenland': {'short_name': 'BL', 'search_pattern': r'^Bgld\.'},
        'Carinthia': {'short_name':  'K', 'search_pattern': r'^Kt\.'},
        'Lower Austria': {'short_name': 'NO', 'search_pattern': r'^NÖ'},
        'Upper Austria': {'short_name': 'OO', 'search_pattern': r'^OÖ'},
        'Salzburg': {'short_name': 'SB', 'search_pattern': r'^Sbg\.'},
        'Styria': {'short_name': 'ST', 'search_pattern': r'^Stmk\.'},
        'Tyrol': {'short_name':  'T', 'search_pattern': r'^T$'},
        'Vorarlberg': {'short_name':  'V', 'search_pattern': r'^Vbg\.'},
        'Vienna': {'short_name':  'W', 'search_pattern': r'^W$'},
    }

    def __init__(self):
        super().__init__("Austria")
        self.provinces = Austria.provinces
        self.url = 'https://www.sozialministerium.at/Informationen-zum-Coronavirus/Neuartiges-Coronavirus-(2019-nCov).html'
        self.total_pattern = r'.sterreich\s+gesamt'

    def get_cov19_data(self) -> str:
        response = requests.get(self.url)
        tables = pd.read_html(response.text, thousands=".", decimal=",")
        self.data['provinces'] = OrderedDict()
        self.get_all_cases(tables[0])

        self.check_data()
        return self.get_data_as_json()

    def get_all_cases(self, df: pd.DataFrame):
        at_all = df.filter(regex=self.total_pattern)
        self.data['c'] = int(at_all.iloc[0])
        self.data['d'] = int(at_all.iloc[1])
        self.get_cases_by_province(df)
        self.get_deaths_by_province(df)

    def get_cases_by_province(self, df: pd.DataFrame) -> None:
        return self._get_numbers_by_province('c', df)

    def get_deaths_by_province(self, df: pd.DataFrame) -> None:
        return self._get_numbers_by_province('d', df)

    def _get_numbers_by_province(self, what: str, df: pd.DataFrame) -> None:
        if what not in ['c', 'd']:
            raise ValueError("Don't know what to look for, invalid pattern.")
        for province in self.provinces.keys():
            short_name = self.provinces[province]["short_name"]
            pattern = self.provinces[province]["search_pattern"]
            if what == 'c':
                case_idx = 0
            else:
                case_idx = 1
            province_cases = df.filter(regex=pattern)
            cases = int(province_cases.iloc[case_idx])
            if not self.data.get('provinces'):
                self.data['provinces'] = OrderedDict()
            if not self.data['provinces'].get(short_name):
                self.data['provinces'][short_name] = OrderedDict()
            self.data['provinces'][short_name][what] = cases
