import pytest
import mock
import json
import responses
import pathlib
from cov19.collect import Austria
from .helpers import assert_if_province_data_is_equal, assert_if_provinces_have_no_cases_and_deaths


base_path = pathlib.Path(__file__).parent.parent


@pytest.fixture()
def at():
    austria = Austria()
    yield austria


@responses.activate
def test_get_cov19_data_returns_values(at: Austria):
    with open("{}/res/at_fallzahlen.html".format(base_path)) as f:
        body = f.read()
        responses.add(responses.GET, at.url, body=body, status=200)
        raw_data = at.get_cov19_data()
        data = json.loads(raw_data)

        assert data['country'] == "AT"
        assert 'c' in data, "Could not find 'cases'"
        assert data['c'] >= 13561, 'Invalid number for cases in AT'.format(14451, data['c'])

        assert 'd' in data, "Could not find 'deaths'"
        assert data['d'] >= 337, 'Invalid number for deaths in AT'.format(410, data['d'])

        assert_if_provinces_have_no_cases_and_deaths(at, data)
        assert_if_province_data_is_equal(at, data)


@mock.patch('cov19.collect.Austria._get_numbers_by_province')
def test_get_deaths_by_province_calls_correct_func(mock_get, at):
    at.get_deaths_by_province("deaths")
    mock_get.assert_called_once_with('d', 'deaths')


@mock.patch('cov19.collect.Austria._get_numbers_by_province')
def test_get_cases_by_province_calls_correct_func(mock_get, at):
    at.get_cases_by_province("cases")
    mock_get.assert_called_once_with('c', 'cases')


@mock.patch('cov19.collect.Austria.get_cases_by_province')
@mock.patch('cov19.collect.Austria.get_deaths_by_province')
@mock.patch('pandas.DataFrame')
def test_get_all_cases_calls_correct_funcs(mock_df, mock_d, mock_c, at):
    mock_iloc = mock.MagicMock()
    mock_df.filter.return_value = mock_iloc

    at.get_all_cases(mock_df)

    mock_df.filter.assert_called_once_with(regex=at.total_pattern)
    mock_c.assert_called_once_with(mock_df)
    mock_d.assert_called_once_with(mock_df)
