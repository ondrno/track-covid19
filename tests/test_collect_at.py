import json
import responses
import pathlib
from cov19 import Austria


base_path = pathlib.Path(__file__).parent


@responses.activate
def test_get_data_returns_values():
    expected = {"country": "AT",
                "provinces": {
                    "BL": {"c": 138, "d": 2},
                    "K": {"c": 202, "d": 2},
                    "NO": {"c": 1217, "d": 4},
                    "OO": {"c": 1217, "d": 4},
                    "SB": {"c": 687, "d": 1},
                    "ST": {"c": 759, "d": 13},
                    "T": {"c": 1752, "d": 6},
                    "V": {"c": 501, "d": 1},
                    "W": {"c": 1003, "d": 16}
                }, "c": 7399, "d": 58}
    at = Austria()
    with open("{}/res/at_fallzahlen.html".format(base_path)) as f:
        body = f.read()
        responses.add(responses.GET, at.url, body=body, status=200)
        data = at.get_cov19_data()

        assert data == json.dumps(expected)


@responses.activate
def test_get_data_returns_empty_list():
    at = Austria()
    with open("{}/res/de_fallzahlen.html".format(base_path)) as f:
        body = f.read()
        responses.add(responses.GET, at.url, body=body, status=200)
        data = at.get_cov19_data()

        assert data == json.dumps({})
