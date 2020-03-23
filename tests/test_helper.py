import pytest
import mock
from cov19 import get_query_interval
from cov19.helper import _interval_to_ms


def test_interval_to_ms_raises_exception():
    with pytest.raises(ValueError):
        _interval_to_ms(10, 'z')


@pytest.mark.parametrize("value", ["29m", "25h", None])
@mock.patch('os.environ.get')
def test_query_interval_casts_valid_units_to_default(mock_get, value):
    mock_get.return_value = value
    four_hours_in_ms = 4 * 60 * 60 * 1000

    interval = get_query_interval()
    assert four_hours_in_ms == interval


@pytest.mark.parametrize("value, exp_ms", [("30m", 1800000), ("24h", 86400000)])
@mock.patch('os.environ.get')
def test_query_interval_returns_set_env_values(mock_get, value, exp_ms):
    mock_get.return_value = value
    interval = get_query_interval()
    assert exp_ms == interval


@pytest.mark.parametrize("value", ["29s", "13d"])
@mock.patch('os.environ.get')
def test_query_interval_raises_exception_for_values_with_invalid_units(mock_get, value):
    mock_get.return_value = value
    with pytest.raises(ValueError):
        get_query_interval()
