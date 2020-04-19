import json
from datetime import datetime
import pathlib
from loguru import logger
from cov19.collect import DataCollector


class Cov19Statistics:
    def __init__(self, log_file: str = "log/cov19_stats.log"):
        self.base_path = pathlib.Path(__file__).parent.parent
        self.log_file = self.base_path.joinpath(log_file)
        self.countries = []
        self.statistics = []
        self.do_run = False

    def add_country(self, country: object) -> None:
        if not isinstance(country, DataCollector):
            raise ValueError("Country has to be a DataCollector object")
        if country not in self.countries:
            self.countries.append(country)

    def remove_country(self, country: object) -> None:
        if country in self.countries:
            self.countries.remove(country)

    def write_statistics_to_file(self) -> None:
        self.get_todays_statistics()

        with open(self.log_file, 'a') as f:
            for stat in self.statistics:
                f.write(stat + "\n")

    def get_todays_statistics(self) -> None:
        for country in self.countries:
            try:
                country.get_cov19_data()
                country.data['date'] = self._get_datetime_now_as_iso()
                self.statistics.append(country.get_data_as_json())
                logger.info(country.get_data_as_json())
            except:
                logger.error("Could not get data for country={}".format(country))
                pass

    def _get_datetime_now_as_iso(self) -> str:
        today = datetime.now()
        today = datetime(today.year, today.month, today.day, today.hour, today.minute).isoformat()
        return today

    def run(self):
        self.write_statistics_to_file()
