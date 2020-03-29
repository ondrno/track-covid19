import pytest
import mock
import re
import pathlib
from cov19 import Cov19Statistics
from cov19.collect import Austria, DataCollector


base_path = pathlib.Path(__file__).parent.parent


@pytest.fixture()
def cov():
    cov = Cov19Statistics()
    yield cov


def test_add_country_adds_country_if_not_yet_there(cov):
    at = Austria()
    cov.add_country(at)
    assert len(cov.countries) == 1
    assert isinstance(cov.countries[0], DataCollector)
    assert at in cov.countries


def test_add_country_adds_country_only_once(cov):
    at = Austria()
    cov.add_country(at)
    cov.add_country(at)
    assert len(cov.countries) == 1
    assert isinstance(cov.countries[0], DataCollector)
    assert at in cov.countries


def test_add_country_raises_exception_for_wrong_object(cov):
    with pytest.raises(ValueError):
        cov.add_country(cov)


def test_remove_country_removes_country_if_there(cov):
    at = Austria()
    cov.add_country(at)
    assert len(cov.countries) == 1
    assert at in cov.countries

    cov.remove_country(at)
    assert len(cov.countries) == 0
    assert at not in cov.countries


def test_remove_country_does_nothing_if_not_there(cov):
    at = Austria()
    cov.add_country(at)
    assert len(cov.countries) == 1
    assert at in cov.countries

    cov.remove_country("foo")
    assert len(cov.countries) == 1
    assert at in cov.countries


@mock.patch('cov19.collect.Austria.get_cov19_data')
@mock.patch('cov19.statistics.Cov19Statistics._get_datetime_now_as_iso')
@mock.patch('json.dumps')
def test_get_todays_statistics_get_stats(mock_dumps, mock_date, mock_get, cov):
    at = Austria()
    cov.add_country(at)
    cov.get_todays_statistics()

    mock_get.assert_called_once()
    mock_date.assert_called_once()
    # json.dumps will be called with empty dict because get_cov19_data() did not fill 'c' and 'd' keys
    calls = [mock.call({})]
    mock_dumps.assert_has_calls(calls, any_order=True)


@mock.patch('cov19.statistics.Cov19Statistics.write_statistics_to_file')
def test_run_calls_write_statistics(mock_write, cov):
    cov.run()
    mock_write.assert_called_once()


def test_get_datetime_now_as_iso_matches_regex(cov):
    today = cov._get_datetime_now_as_iso()
    assert re.match(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:00', today)
