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
        p = soup.find(id='covid-19-cases-total')
        if p:
            m = re.search(r'([\d,]+)', p.get_text(), re.I | re.M)
            if m:
                cases = m.group(1)
                cases = int(cases.replace(",", ""))
                self.data['c'] = cases

        p = soup.find(id='covid-19-deaths-total')
        if p:
            m = re.search(r'([\d,]+)', p.get_text(), re.I | re.M)
            if m:
                deaths = m.group(1)
                deaths = int(deaths.replace(",", ""))
                self.data['d'] = deaths

        self.check_data()
        return self.get_data_as_json()
