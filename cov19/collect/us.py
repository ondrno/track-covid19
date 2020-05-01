import requests
import re
from bs4 import BeautifulSoup
from cov19.collect import DataCollector


class UnitedStates(DataCollector):
    def __init__(self):
        super().__init__("United States")
        self.url = "https://www.cdc.gov/coronavirus/2019-ncov/cases-updates/cases-in-us.html?CDC_AA_refVal=https%3A%2F%2Fwww.cdc.gov%2Fcoronavirus%2F2019-ncov%2Fcases-in-us.html"

    def get_cov19_data(self):
        response = requests.get(self.url)
        soup = BeautifulSoup(response.text, "html.parser")
        p = soup.findAll("div", {"class": 'callout'})
        for totals in p:
            text = totals.get_text()
            m = re.search(r'Total\s(cases|deaths)[\s\S]+?([\d,]+)', text, re.I | re.M)
            if m:
                cases_type = m.group(1)
                raw_cases = m.group(2)
                cases = int(raw_cases.replace(",", ""))
                if cases_type.lower() == 'cases':
                    self.data['c'] = cases
                else:
                    self.data['d'] = cases

        self.check_data()
        return self.get_data_as_json()
