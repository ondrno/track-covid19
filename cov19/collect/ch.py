import requests
import re
from bs4 import BeautifulSoup
from cov19 import DataCollector


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
