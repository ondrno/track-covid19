import pytest
import responses
import pathlib
from cov19 import Cov19Statistics


base_path = pathlib.Path(__file__).parent

@pytest.mark.parametrize("data, exp_str", [([1, 2], "1;2"), ([], ""), (["a", "b"], "a;b")])
def test_list2str_returns_empty_string_for_empty_list(data, exp_str):
    c = Cov19Statistics()
    data_as_str = c._list2str(data)
    assert data_as_str == exp_str


def test_get_data_germany_returns_values():
    c = Cov19Statistics()
    c.url_de = "{}/res/de_fallzahlen.html".format(base_path)
    data = c.get_data_germany()
    assert data == [2369, 5]


def test_get_data_germany_emtpy_list():
    c = Cov19Statistics()
    c.url_de = "{}/res/at_fallzahlen.html".format(base_path)
    data = c.get_data_germany()
    assert data == []


@responses.activate
def test_get_data_austria_returns_values():
    c = Cov19Statistics()
    with open("{}/res/at_fallzahlen.html".format(base_path)) as f:
        body = f.read()
        responses.add(responses.GET, c.url_at, body=body, status=200)
        data = c.get_data_austria()
        assert data == [361, 1, 4]


@responses.activate
def test_get_data_austria_returns_empty_list():
    c = Cov19Statistics()
    with open("{}/res/de_fallzahlen.html".format(base_path)) as f:
        body = f.read()
        responses.add(responses.GET, c.url_at, body=body, status=200)
        data = c.get_data_austria()
        assert data == []


@responses.activate
def test_get_data_switzerland_returns_values():
    c = Cov19Statistics()
    with open("{}/res/ch_fallzahlen.html".format(base_path)) as f:
        body = f.read()
        responses.add(responses.GET, c.url_ch, body=body, status=200)
        data = c.get_data_switzerland()
        assert data == [1359, 11]
