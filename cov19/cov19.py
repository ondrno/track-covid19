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
            f.write(statistics + "\n")

    def get_todays_statistics(self) -> str:
        today = datetime.now()
        today_as_str = self._list2str([today.year, today.month, today.day, today.hour, today.minute])

        de_data = self.get_data_germany()
        de_as_str = self._list2str(de_data)

        at_data = self.get_data_austria()
        at_as_str = self._list2str(at_data)

        stats = "{};{};{};{};{}".format(today_as_str, "DE", de_as_str, "AT", at_as_str)
        return stats

    @staticmethod
    def get_header_info():
        return "year;month;day;hour;minute;DE;cases;dead;AT;cases;recovered;dead"

    def get_data_germany(self):
        stats = []
        try:
            tables = pd.read_html(self.url_de)

            title = tables[0].columns[1]
            raw_cases = tables[0][title][16]
            m = re.match(r'([\d\.]+)\s*\(([\d\.]+)\)', raw_cases)
            if m:
                cases = self._str2int(m.group(1))
                death = self._str2int(m.group(2))

            stats.append(cases)
            stats.append(death)
        except ValueError:
            pass

        if not stats:
            logger.error("Could not obtain statistics for Germany")
        return stats

    def get_data_austria(self):
        stats = []
        response = requests.get(self.url_at)
        soup = BeautifulSoup(response.text, "html.parser")
        for p in soup.find_all('p'):
            m = re.search(r'.*Bestätigte Fälle:\s*(\d+).+\s+Genesene Personen:\s*(\d+).+\s+Todesfälle:\s*(\d+).*', str(p),
                          re.I | re.M)
            if m:
                cases = int(m.group(1))
                recovered = int(m.group(2))
                death = int(m.group(3))
                stats.append(cases)
                stats.append(recovered)
                stats.append(death)
                break
        if not stats:
            logger.error("Could not obtain statistics for Austria")
        return stats

    def run(self):
        self.write_statistics_to_file()


if __name__ == "__main__":
    import argparse

    version = "1.0.1"
    parser = argparse.ArgumentParser(description="Program which tracks the SARS-Cov-2 infection "
                                                 "rate in Germany and Austria")
    parser.add_argument("--version", action='version', version=version)
    parser.add_argument("log_file", default="cov19_statistics.log", help="the file to log statistics into", type=str)
    args = parser.parse_args()

    cov19 = Cov19Statistics(args.log_file)
    cov19.run()
