import pytest
import json
import pathlib
from cov19.collect import DataCollector


base_path = pathlib.Path(__file__).parent


@pytest.fixture()
def dc():
    dc = DataCollector("Germany")
    yield dc


def test_init_raises_exception_if_unknown_country():
    with pytest.raises(ValueError):
        DataCollector("Sweden")


def test_init_sets_vars(dc):
    assert dc.get_name() == "Germany"
    assert dc.provinces == {}


def test_get_cov19_data_returns_self_data(dc):
    assert dc.get_cov19_data() == {'country': 'DE'}


def test_check_data_returns_true_if_both(dc):
    dc.data = {'c': 1, 'd': 1}
    res = dc.check_data()
    assert res is True


@pytest.mark.parametrize("cov_data", [{'c': 1}, {'d': 1}])
def test_check_data_returns_false_one_missing(cov_data, dc):
    dc.data = cov_data
    res = dc.check_data()
    assert res is False


def test_get_data_as_json_returns_empty_list_if_data_is_missing(dc):
    res = dc.get_data_as_json()
    assert res == json.dumps({})


def test_get_data_as_json_returns_json_if_valid_data(dc):
    expected = {"country": "DE", 'c': 1, 'd': 2}
    dc.data['c'] = 1
    dc.data['d'] = 2
    res = dc.get_data_as_json()
    assert res == json.dumps(expected)
