import pandas as pd
from datetime import datetime
from loguru import logger
import requests
import re
import pathlib
from bs4 import BeautifulSoup


class Cov19Statistics:
    def __init__(self, log_file: str = "cov19_statistics.log"):
        self.log_file = pathlib.Path(log_file)
        self.url_de = "https://www.rki.de/DE/Content/InfAZ/N/Neuartiges_Coronavirus/Fallzahlen.html"
        self.url_at = "https://www.sozialministerium.at/Informationen-zum-Coronavirus/Neuartiges-Coronavirus-(2019-nCov).html"
        self.url_ch = "https://www.bag.admin.ch/bag/de/home/krankheiten/ausbrueche-epidemien-pandemien/aktuelle-ausbrueche-epidemien/novel-cov/situation-schweiz-und-international.html"
        self.url_uk = "https://www.arcgis.com/sharing/rest/content/items/bc8ee90225644ef7a6f4dd1b13ea1d67/data"
        self.url_us = "https://www.cdc.gov/coronavirus/2019-ncov/cases-updates/cases-in-us.html?CDC_AA_refVal=https%3A%2F%2Fwww.cdc.gov%2Fcoronavirus%2F2019-ncov%2Fcases-in-us.html"
        self.statistics = []
        self.do_run = False

    def _str2int(self, value) -> int:
        return int(str(value).replace(".", ""))

    def _list2str(self, data: list) -> str:
        data_as_str = ";".join(map(lambda x: str(x), data))
        return data_as_str

    def write_statistics_to_file(self) -> None:
        header = ''
        statistics = self.get_todays_statistics()
        logger.info(statistics)

        if not self.log_file.exists():
            header = self.get_header_info()
        with open(self.log_file, 'a') as f:
            if header:
                f.write(header + "\n")
            for stat in statistics:
                f.write(stat + "\n")

    def get_todays_statistics(self) -> str:
        today = datetime.now()
        today_as_str = self._list2str([today.year, today.month, today.day, today.hour, today.minute])

        de_data = self.get_data_germany()
        de_as_str = self._list2str(de_data)

        at_data = self.get_data_austria()
        at_as_str = self._list2str(at_data)

        ch_data = self.get_data_switzerland()
        ch_as_str = self._list2str(ch_data)

        uk_data = self.get_data_united_kingdom()
        uk_as_str = self._list2str(uk_data)

        us_data = self.get_data_united_states()
        us_as_str = self._list2str(us_data)

        stats = list()
        stats.append("{};{};{}".format(today_as_str, "DE", de_as_str))
        stats.append("{};{};{}".format(today_as_str, "AT", at_as_str))
        stats.append("{};{};{}".format(today_as_str, "CH", ch_as_str))
        stats.append("{};{};{}".format(today_as_str, "UK", uk_as_str))
        stats.append("{};{};{}".format(today_as_str, "US", us_as_str))
        return stats

    @staticmethod
    def get_header_info():
        return "year;month;day;hour;minute;country;cases;deaths;recovered"

    def get_data_germany(self):
        stats = []
        response = requests.get(self.url_de)
        if response.status_code == 200:
            try:
                tables = pd.read_html(response.text)
                cases_title = tables[0].columns[1]
                cases = tables[0][cases_title][16]
                cases = self._str2int(cases)

                deaths_title = tables[0].columns[4]
                deaths = tables[0][deaths_title][16]
                deaths = self._str2int(deaths)

                stats.append(cases)
                stats.append(deaths)
            except ValueError:
                pass
            if not stats:
                logger.error("Could not find numbers in web page for Germany")
        else:
            logger.error("Could not access statistics for Germany (status code={})".format(response.status_code))
        return stats

    def get_data_austria(self):
        stats = []
        response = requests.get(self.url_at)
        soup = BeautifulSoup(response.text, "html.parser")
        cases = deaths = recovered = None
        for p in soup.find_all('p'):
            m = re.search(r'Best.+tigte F.+lle:.+?([\d.]+)', str(p), re.I | re.M)
            if m:
                cases = self._str2int(m.group(1))
                stats.append(cases)

            m = re.search(r'Todesf.+lle:.+?([\d.]+)', str(p), re.I | re.M)
            if m:
                deaths = self._str2int(m.group(1))
                stats.append(deaths)

            m = re.search(r'Genesene Personen:.+?([\d.]+)', str(p), re.I | re.M)
            if m:
                recovered = self._str2int(m.group(1))
                stats.append(recovered)

            if cases and deaths and recovered:
                break
        if not stats:
            logger.error("Could not obtain statistics for Austria")
        return stats

    def get_data_switzerland(self):
        stats = []
        response = requests.get(self.url_ch)
        soup = BeautifulSoup(response.text, "html.parser")
        cases = None
        deaths = None
        for p in soup.find_all('p'):
            m = re.search(r'Positiv getestet:\s*(\d+)\s+Personen', str(p), re.I | re.M)
            if m:
                cases = int(m.group(1))
                stats.append(cases)
                next

            m = re.search(r'Verstorben:.+?(\d+)\s+Personen', str(p), re.I | re.M)
            if m:
                deaths = int(m.group(1))
                stats.append(deaths)

            if cases and deaths:
                break

        if not stats:
            logger.error("Could not obtain statistics for Switzerland")
        return stats

    def get_data_united_kingdom(self):
        stats = []
        try:
            tables = pd.read_excel(self.url_uk)
            cases = tables.iloc[0]['TotalUKCases']
            deaths = tables.iloc[0]['TotalUKDeaths']
            stats.append(int(cases))
            stats.append(int(deaths))
        except KeyError:
            pass

        if not stats:
            logger.error("Could not obtain statistics for United Kingdom")
        return stats

    def get_data_united_states(self):
        stats = []
        response = requests.get(self.url_us)
        soup = BeautifulSoup(response.text, "html.parser")
        cases = None
        deaths = None
        for p in soup.find_all('li'):
            m = re.search(r'Total cases:\s*([\d,]+)', str(p), re.I | re.M)
            if m:
                cases = m.group(1)
                cases = int(cases.replace(",", ""))
                stats.append(cases)
                next

            m = re.search(r'Total deaths:.+?(\d+)', str(p), re.I | re.M)
            if m:
                deaths = m.group(1)
                deaths = int(deaths.replace(",", ""))
                stats.append(deaths)

            if cases and deaths:
                break

        if not stats:
            logger.error("Could not obtain statistics for United States")
        return stats

    def run(self):
        self.write_statistics_to_file()


if __name__ == "__main__":
    import argparse

    version = "1.0.5"
    parser = argparse.ArgumentParser(description="Program which tracks the SARS-Cov-2 infection rate in "
                                                 "Germany, Austria, Switzerland, United Kingdom, United States")
    parser.add_argument("--version", action='version', version=version)
    parser.add_argument("log_file", default="cov19_statistics.log", help="the file to log statistics into", type=str)
    args = parser.parse_args()

    cov19 = Cov19Statistics(args.log_file)
    cov19.run()
