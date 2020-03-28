import json
import responses
import pathlib
from cov19 import Germany


base_path = pathlib.Path(__file__).parent


@responses.activate
def test_get_data_returns_values():
    expected = {"country": "DE", "c": 18610, "d": 55}
    de = Germany()
    with open("{}/res/de_fallzahlen.html".format(base_path)) as f:
        body = f.read()
        responses.add(responses.GET, de.url, body=body, status=200)
        data = de.get_cov19_data()

        assert data == json.dumps(expected)


@responses.activate
def test_get_data_returns_empty_list():
    de = Germany()
    with open("{}/res/at_fallzahlen.html".format(base_path)) as f:
        body = f.read()
        responses.add(responses.GET, de.url, body=body, status=200)
        data = de.get_cov19_data()

        assert data == json.dumps({})
