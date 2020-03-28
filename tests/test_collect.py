import pytest
import json
import pathlib
from cov19.collect import DataCollector


base_path = pathlib.Path(__file__).parent


def test_check_data_returns_true():
    d = DataCollector("Germany")
    d.data['c'] = 1
    d.data['d'] = 1
    res = d.check_data()
    assert res is True


@pytest.mark.parametrize("cov_data", [{'c': 1}, {'d': 1}])
def test_check_data_returns_false(cov_data):
    d = DataCollector("Germany")
    d.data = cov_data
    res = d.check_data()
    assert res is False


def test_get_data_as_json_returns_empty_list_if_data_is_missing():
    d = DataCollector("Germany")
    res = d.get_data_as_json()
    assert res == json.dumps({})


def test_get_data_as_json_returns_json_if_valid_data():
    expected = {"country": "DE", 'c': 1, 'd': 2}
    d = DataCollector("Germany")
    d.data['c'] = 1
    d.data['d'] = 2
    res = d.get_data_as_json()
    assert res == json.dumps(expected)
