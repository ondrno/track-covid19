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


@responses.activate
def test_get_data_germany_returns_values():
    c = Cov19Statistics()
    with open("{}/res/de_fallzahlen.html".format(base_path)) as f:
        body = f.read()
        responses.add(responses.GET, c.url_de, body=body, status=200)
        data = c.get_data_germany()
        assert data == [18610, 55]


@responses.activate
def test_get_data_germany_returns_empty_list():
    c = Cov19Statistics()
    with open("{}/res/at_fallzahlen.html".format(base_path)) as f:
        body = f.read()
        responses.add(responses.GET, c.url_de, body=body, status=200)
        data = c.get_data_germany()
        assert data == []


@responses.activate
def test_get_data_austria_returns_values():
    c = Cov19Statistics()
    with open("{}/res/at_fallzahlen.html".format(base_path)) as f:
        body = f.read()
        responses.add(responses.GET, c.url_at, body=body, status=200)
        data = c.get_data_austria()
        assert data == [7399, 58]


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
        assert data == [10714, 161]


def test_get_data_uk_returns_values():
    c = Cov19Statistics()
    c.url_uk = "{}/res/uk_fallzahlen.xlsx".format(base_path)
    data = c.get_data_united_kingdom()
    assert data == [797, 10]


@responses.activate
def test_get_data_us_returns_values():
    c = Cov19Statistics()
    with open("{}/res/us_fallzahlen.html".format(base_path)) as f:
        body = f.read()
        responses.add(responses.GET, c.url_us, body=body, status=200)
        data = c.get_data_united_states()
        assert data == [1629, 41]


def test_get_header_info_returns_string():
    assert "dt;country;cases;deaths;recovered" == Cov19Statistics.get_header_info()