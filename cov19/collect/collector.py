import json
import pandas as pd
import requests
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
        self.provinces = {}

    def get_cov19_data(self):
        return self.data

    def get_name(self):
        return self.country

    def check_data(self):
        if 'c' in self.data and 'd' in self.data:
            return True
        else:
            logger.error("Could not find cases/deaths numbers in web page for {}".format(self.country))
            return False

    def get_data_as_json(self):
        """ Returns self.data as json string unless the dict contains no 'c' (cases) or no 'd' (deaths)"""
        if 'c' in self.data or 'd' in self.data:
            return json.dumps(self.data)
        else:
            return json.dumps({})

    def _str2int(self, value, thousands=".") -> int:
        return int(str(value).replace(thousands, ""))
