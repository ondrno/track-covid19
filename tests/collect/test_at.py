import pytest
import mock
import json
import responses
import pathlib
from cov19.collect import Austria


base_path = pathlib.Path(__file__).parent.parent


@pytest.fixture()
def at():
    austria = Austria()
    yield austria


@responses.activate
def test_get_cov19_data_returns_values(at: Austria):
    expected = {"country": "AT",
                "provinces": {
                    "BL": {"c": 234, "d": 3},
                    "K": {"c": 341, "d": 4},
                    "NO": {"c": 2071, "d": 39},
                    "OO": {"c": 1991, "d": 23},
                    "SB": {"c": 1094, "d": 16},
                    "ST": {"c": 1372, "d": 60},
                    "T": {"c": 2835, "d": 40},
                    "V": {"c": 768, "d": 5},
                    "W": {"c": 1813, "d": 53}
                }, "c": 12519, "d": 243}
    with open("{}/res/at_fallzahlen.html".format(base_path)) as f:
        body = f.read()
        responses.add(responses.GET, at.url, body=body, status=200)
        data = at.get_cov19_data()

        assert data == json.dumps(expected)


def test_get_re_pattern_for_province_invalid_what(at):
    with pytest.raises(ValueError):
        at._get_re_pattern_for_province('f', 'Burgenland')


def test_get_re_pattern_for_province_invalid_province(at):
    with pytest.raises(ValueError):
        at._get_re_pattern_for_province('c', 'WienerLand')


@pytest.mark.parametrize("what, exp_pattern", [
    ('c', 'Best.+tigte F.+lle.+?Uhr.*?:.*?([\\d.]+) F.+lle.+?Steiermark.+?(([\\d.]+))'),
    ('d', 'Todesf.+lle.+?Uhr:.*?([\\d.]+).+?Steiermark.+?(([\\d.]+))')
])
def test_get_re_pattern_for_province_styria(at, what, exp_pattern):
    pattern = at._get_re_pattern_for_province(what, 'Styria')
    assert pattern == exp_pattern


@pytest.mark.parametrize("what, number", [('c', '42'), ('d', '42')])
@mock.patch('cov19.collect.Austria._get_re_pattern_for_province')
@mock.patch('cov19.collect.Austria._str2int')
def test_get_numbers_by_province_for_burgenland_if_match(mock_str2int, mock_re, what, number, at):
    string = "foo - {}".format(number)
    mock_str2int.return_value = 10
    mock_re.return_value = r'(foo) - (\d+)'
    at.provinces = {'Burgenland': {'short_name': 'BL', 'search_pattern': r'Burgenland'}}

    at._get_numbers_by_province(what, string)
    assert at.data['provinces']['BL'][what] == 10
    mock_str2int.assert_called_once_with(number)
    mock_re.assert_called_once_with(what, 'Burgenland')


@mock.patch('cov19.collect.Austria._get_numbers_by_province')
def test_get_deaths_by_province_calls_correct_func(mock_get, at):
    at.get_deaths_by_province("deaths")
    mock_get.assert_called_once_with('d', 'deaths')


@mock.patch('cov19.collect.Austria._get_numbers_by_province')
def test_get_cases_by_province_calls_correct_func(mock_get, at):
    at.get_cases_by_province("cases")
    mock_get.assert_called_once_with('c', 'cases')


@mock.patch('cov19.collect.Austria._get_total_numbers')
def test_get_total_cases_calls_correct_func(mock_get, at):
    at.get_total_cases("total_cases")
    mock_get.assert_called_once_with('c', 'total_cases')


@mock.patch('cov19.collect.Austria._get_total_numbers')
def test_get_total_deaths_calls_correct_func(mock_get, at):
    at.get_total_deaths("total_deaths")
    mock_get.assert_called_once_with('d', 'total_deaths')


