import requests
import pandas as pd
from loguru import logger
from cov19.collect import DataCollector


class UnitedStates(DataCollector):
    def __init__(self):
        super().__init__("United States")
        self.url = "https://github.com/nytimes/covid-19-data/blob/master/live/us.csv"

    def get_cov19_data(self):
        response = requests.get(self.url)
        try:
            tables = pd.read_html(response.text)
            self.get_all_cases(tables[0])
        except ValueError:
            logger.error("Could not obtain covid19 information for the US. Data source invalid.")

        self.check_data()
        return self.get_data_as_json()

    def get_all_cases(self, df: pd.DataFrame):
        self.data['c'] = int(df['cases'][0])
        self.data['d'] = int(df['deaths'][0])
