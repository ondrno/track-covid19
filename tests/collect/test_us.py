import mock
import json
import responses
import pathlib
from cov19.collect import UnitedStates


base_path = pathlib.Path(__file__).parent.parent


@responses.activate
def test_get_cov19_data_returns_values():
    us = UnitedStates()
    with open("{}/res/us_fallzahlen.html".format(base_path)) as f:
        body = f.read()
        responses.add(responses.GET, us.url, body=body, status=200)
        data = us.get_cov19_data()

        assert data == json.dumps({"country": "US", 'c': 7828007, 'd': 214879})


@mock.patch('cov19.collect.UnitedStates.check_data')
@responses.activate
def test_get_cov19_data_returns_empty_list_if_no_li_found(mock_check):
    us = UnitedStates()
    body = "<html></html>"
    responses.add(responses.GET, us.url, body=body, status=200)
    data = us.get_cov19_data()
    assert data == json.dumps({})
    mock_check.assert_called()
