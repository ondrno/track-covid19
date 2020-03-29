import pandas as pd
from cov19.collect import DataCollector


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
