import json
from datetime import datetime
import pathlib
from loguru import logger


class Cov19Statistics:
    def __init__(self, log_file: str = "log/cov19_stats.log"):
        self.base_path = pathlib.Path(__file__).parent.parent
        self.log_file = self.base_path.joinpath(log_file)
        self.countries = []
        self.statistics = []
        self.do_run = False

    def add_country(self, country):
        if country not in self.countries:
            self.countries.append(country)

    def remove_country(self, country):
        if country in self.countries:
            self.countries.remove(country)

    def write_statistics_to_file(self) -> None:
        self.get_todays_statistics()

        with open(self.log_file, 'a') as f:
            for stat in self.statistics:
                f.write(stat + "\n")

    def get_todays_statistics(self) -> str:
        today = datetime.now()
        today = datetime(today.year, today.month, today.day, today.hour, today.minute).isoformat()

        for country in self.countries:
            country.get_cov19_data()
            country.data['date'] = today
            self.statistics.append(country.get_data_as_json())
            logger.info(country.get_data_as_json())

    def run(self):
        self.write_statistics_to_file()
