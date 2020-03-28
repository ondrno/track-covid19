import json
import pandas as pd
import requests
import re
from bs4 import BeautifulSoup
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


class Austria(DataCollector):
    provinces_pattern = {
        'BL': r'Burgenland',
        'K': r'K.+rnten',
        'NO': 'Nieder.+reich',
        'OO': 'Ober.+reich',
        'SB': 'Salzburg',
        'ST': 'Steiermark',
        'T': 'Tirol',
        'V': 'Vorarlberg',
        'W': 'Wien',
    }

    def __init__(self):
        super().__init__("Austria")
        self.url = "https://www.sozialministerium.at/Informationen-zum-Coronavirus/Neuartiges-Coronavirus-(2019-nCov).html"

    def get_cov19_data(self):
        response = requests.get(self.url)
        soup = BeautifulSoup(response.text, "html.parser")
        self.data['provinces'] = OrderedDict()
        for p in soup.find_all('p'):
            m = re.search(r'Best.+tigte F.+lle.+Uhr:.*?([\d.]+) F.+lle', str(p), re.I | re.M)
            if m:
                total_cases = self._str2int(m.group(1))
                self.data['c'] = total_cases

            for province, pattern in Austria.provinces_pattern.items():
                m = re.search(r'Best.+tigte F.+lle.+Bundesl.+ndern:.+?' + pattern + r'.+?(([\d.]+))', str(p), re.I | re.M)
                if m:
                    cases = self._str2int(m.group(1))
                    self.data['provinces'][province] = OrderedDict()
                    self.data['provinces'][province]['c'] = cases

            m = re.search(r'Todesf.+lle.+Uhr:.*?([\d.]+)', str(p), re.I | re.M)
            if m:
                deaths = self._str2int(m.group(1))
                self.data['d'] = deaths

            for province, pattern in Austria.provinces_pattern.items():
                m = re.search(r'Todesf.+lle.+Bundesl.+ndern:.+?' + pattern + r'.+?(([\d.]+))', str(p), re.I | re.M)
                if m:
                    deaths = self._str2int(m.group(1))
                    self.data['provinces'][province]['d'] = deaths

        self.check_data()
        return self.get_data_as_json()


class Switzerland(DataCollector):
    def __init__(self):
        super().__init__("Switzerland")
        self.url = "https://www.bag.admin.ch/bag/de/home/krankheiten/ausbrueche-epidemien-pandemien/aktuelle-ausbrueche-epidemien/novel-cov/situation-schweiz-und-international.html"

    def get_cov19_data(self):
        response = requests.get(self.url)
        soup = BeautifulSoup(response.text, "html.parser")
        for p in soup.find_all('p'):
            # the international figures are usually below the swiss figures, thus stop the scanning
            if re.search(r'Ansteckungen mit dem neuen Coronavirus in.+L.+nder oder Regionen', str(p), re.I | re.M):
                break

            m = re.search(r'positiv getestet:[\s\S]+?([\d\s]+)\s+Personen', str(p), re.I | re.M)
            if m:
                cases_raw = re.sub(r'\D', '', m.group(1))
                cases = int(cases_raw)
                self.data['c'] = cases
                next

            m = re.search(r'Verstorben:[\s\S]+?([\d\s]+)\s*Personen', str(p), re.I | re.M)
            if m:
                deaths_raw = re.sub(r'\D', '', m.group(1))
                deaths = int(deaths_raw)
                self.data['d'] = deaths

        self.check_data()
        return self.get_data_as_json()


class UnitedKingdom(DataCollector):
    def __init__(self):
        super().__init__("United Kingdom")
        self.url = "https://www.arcgis.com/sharing/rest/content/items/bc8ee90225644ef7a6f4dd1b13ea1d67/data"

    def get_cov19_data(self):
        try:
            tables = pd.read_excel(self.url)
            cases = tables.iloc[0]['TotalUKCases']
            deaths = tables.iloc[0]['TotalUKDeaths']
            self.data['c'] = int(cases)
            self.data['d'] = int(deaths)
        except KeyError:
            pass

        self.check_data()
        return self.get_data_as_json()


class UnitedStates(DataCollector):
    def __init__(self):
        super().__init__("United States")
        self.url = "https://www.cdc.gov/coronavirus/2019-ncov/cases-updates/cases-in-us.html?CDC_AA_refVal=https%3A%2F%2Fwww.cdc.gov%2Fcoronavirus%2F2019-ncov%2Fcases-in-us.html"

    def get_cov19_data(self):
        response = requests.get(self.url)
        soup = BeautifulSoup(response.text, "html.parser")
        for p in soup.find_all('li'):
            m = re.search(r'Total cases:\s*([\d,]+)', str(p), re.I | re.M)
            if m:
                cases = m.group(1)
                cases = int(cases.replace(",", ""))
                self.data['c'] = cases
                next

            m = re.search(r'Total deaths:.+?([\d,]+)', str(p), re.I | re.M)
            if m:
                deaths = m.group(1)
                deaths = int(deaths.replace(",", ""))
                self.data['d'] = deaths

        self.check_data()
        return self.get_data_as_json()
