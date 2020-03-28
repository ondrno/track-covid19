import pytest
import json
import responses
import pathlib
from cov19 import Switzerland


base_path = pathlib.Path(__file__).parent


@responses.activate
def test_get_data_returns_values():
    ch = Switzerland()
    with open("{}/res/ch_fallzahlen.html".format(base_path)) as f:
        body = f.read()
        responses.add(responses.GET, ch.url, body=body, status=200)
        data = ch.get_cov19_data()

        assert data == json.dumps({"country": "CH", 'c': 10714, 'd': 161})

