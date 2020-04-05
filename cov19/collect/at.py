import requests
import re
from bs4 import BeautifulSoup
from collections import OrderedDict
from cov19.collect import DataCollector


class Austria(DataCollector):
    provinces = {
        'Burgenland': {'short_name': 'BL', 'search_pattern': r'Burgenland'},
        'Carinthia': {'short_name':  'K', 'search_pattern': r'K.+rnten'},
        'Lower Austria': {'short_name': 'NO', 'search_pattern': 'Nieder.+?reich'},
        'Upper Austria': {'short_name': 'OO', 'search_pattern': 'Ober.+?reich'},
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
        self.cases_pattern = r'Best.+tigte F.+lle.+Uhr.+?:.*?([\d.]+) F.+lle'
        self.deaths_pattern = r'Todesf.+lle.+Uhr:.*?([\d.]+)'

    def get_cov19_data(self):
        response = requests.get(self.url)
        soup = BeautifulSoup(response.text, "html.parser")
        self.data['provinces'] = OrderedDict()
        for p in soup.find_all('p'):
            if self.get_total_cases(str(p)):
                self.get_cases_by_province(str(p))

            if self.get_total_deaths(str(p)):
                self.get_deaths_by_province(str(p))

        self.check_data()
        return self.get_data_as_json()

    def get_total_cases(self, s: str) -> bool:
        return self._get_total_numbers('c', s)

    def get_total_deaths(self, s: str) -> bool:
        return self._get_total_numbers('d', s)

    def _get_total_numbers(self, what: str, s: str) -> bool:
        if what not in ['c', 'd']:
            raise ValueError("Don't know what to look for, invalid pattern.")
        if what == 'c':
            pattern = self.cases_pattern
        else:
            pattern = self.deaths_pattern

        m = re.search(pattern, str(s), re.I | re.M)
        if m:
            total = self._str2int(m.group(1))
            self.data[what] = total
            return True
        return False

    def get_cases_by_province(self, s: str) -> None:
        return self._get_numbers_by_province('c', s)

    def get_deaths_by_province(self, s: str) -> None:
        return self._get_numbers_by_province('d', s)

    def _get_numbers_by_province(self, what: str, s: str) -> None:
        if what not in ['c', 'd']:
            raise ValueError("Don't know what to look for, invalid pattern.")
        for province in self.provinces.keys():
            short_name = self.provinces[province]["short_name"]
            pattern = self._get_re_pattern_for_province(what, province)
            m = re.search(pattern, str(s), re.I | re.M)
            if m:
                cases = self._str2int(m.group(2))
                if not self.data.get('provinces'):
                    self.data['provinces'] = OrderedDict()
                if not self.data['provinces'].get(short_name):
                    self.data['provinces'][short_name] = OrderedDict()
                self.data['provinces'][short_name][what] = cases

    def _get_re_pattern_for_province(self, what: str, province: str) -> str:
        if what not in ['c', 'd']:
            raise ValueError("Don't know what to look for, invalid pattern.")
        if province not in self.provinces.keys():
            raise ValueError("Unknown province")
        if what == 'c':
            base = self.cases_pattern
        else:
            base = self.deaths_pattern
        regex = base + r'.+?' + self.provinces[province]['search_pattern'] + r'.+?(([\d.]+))'
        return regex
