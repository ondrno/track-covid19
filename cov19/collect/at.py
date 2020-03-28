import requests
import re
from bs4 import BeautifulSoup
from collections import OrderedDict
from cov19 import DataCollector


class Austria(DataCollector):
    provinces = {
        'Burgenland': {'short': 'BL', 'search_pattern': r'Burgenland'},
        'Carinthia': {'short_name':  'K', 'search_pattern': r'K.+rnten'},
        'Lower Austria': {'short_name': 'NO', 'search_pattern': 'Nieder.+reich'},
        'Upper Austria': {'short_name': 'OO', 'search_pattern': 'Ober.+reich'},
        'Salzburg': {'short_name': 'SB', 'search_pattern': 'Salzburg'},
        'Styria': {'short_name': 'ST', 'search_pattern': 'Steiermark'},
        'Tyrol': {'short_name':  'T', 'search_pattern': 'Tirol'},
        'Vorarlberg': {'short_name':  'V', 'search_pattern': 'Vorarlberg'},
        'Vienna': {'short_name':  'W', 'search_pattern': 'Wien'},
    }

    def __init__(self):
        super().__init__("Austria")
        self.provinces = Austria.provinces
        self.url = "https://www.sozialministerium.at/Informationen-zum-Coronavirus/Neuartiges-Coronavirus-(2019-nCov).html"
        self.cases_pattern = r'Best.+tigte F.+lle.+Uhr:.*?([\d.]+) F.+lle'
        self.deaths_pattern = r'Todesf.+lle.+Uhr:.*?([\d.]+)'

    def _get_re_pattern(self, what: str, province: str) -> str:
        if what not in ['c', 'd']:
            raise ValueError("Invalid type of re pattern")
        if province not in self.provinces.keys():
            raise ValueError("Unknown province")
        if what == 'c':
            base = self.cases_pattern
        else:
            base = self.deaths_pattern
        regex = base + self.provinces[province]['search_pattern'] + r'.+?(([\d.]+))'
        return regex

    def get_cases_by_province(self, s: str) -> None:
        for province in self.provinces.keys():
            m = re.search(self._get_re_pattern('c', province), str(s), re.I | re.M)
            if m:
                cases = self._str2int(m.group(1))
                self.data['provinces'][province] = OrderedDict()
                self.data['provinces'][province]['c'] = cases

    def get_deaths_by_province(self, s: str) -> None:
        for province in Austria.provinces.keys():
            m = re.search(self._get_re_pattern('d', province), str(s), re.I | re.M)
            if m:
                cases = self._str2int(m.group(1))
                self.data['provinces'][province] = OrderedDict()
                self.data['provinces'][province]['d'] = cases

    def get_total_cases(self, s: str) -> None:
        m = re.search(self.cases_pattern, str(s), re.I | re.M)
        if m:
            total = self._str2int(m.group(1))
            self.data['c'] = total

    def get_total_deaths(self, s: str) -> None:
        m = re.search(self.deaths_pattern, str(s), re.I | re.M)
        if m:
            total = self._str2int(m.group(1))
            self.data['d'] = total

    def get_cov19_data(self):
        response = requests.get(self.url)
        soup = BeautifulSoup(response.text, "html.parser")
        self.data['provinces'] = OrderedDict()
        for p in soup.find_all('p'):
            self.get_total_cases(str(p))
            self.get_cases_by_province(str(p))

            self.get_total_deaths(str(p))
            self.get_deaths_by_province(str(p))

        self.check_data()
        return self.get_data_as_json()
