import pytest
import json
import responses
import pathlib
from cov19.collect import UnitedStates


base_path = pathlib.Path(__file__).parent.parent


@responses.activate
def test_get_data_returns_values():
    us = UnitedStates()
    with open("{}/res/us_fallzahlen.html".format(base_path)) as f:
        body = f.read()
        responses.add(responses.GET, us.url, body=body, status=200)
        data = us.get_cov19_data()

        assert data == json.dumps({"country": "US", 'c': 85356, 'd': 1246})
