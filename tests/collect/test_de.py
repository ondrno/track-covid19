import json
import responses
import pathlib
from cov19.collect import Germany


base_path = pathlib.Path(__file__).parent.parent


@responses.activate
def test_get_data_returns_values():
    expected = {"country": "DE", "c": 18610, "d": 55,
                "provinces": {
                    "BW": {"c": 3807, "d": 21}, "BY": {"c": 3650, "d": 21},
                    "BE": {"c": 1024, "d": 1}, "BB": {"c": 274, "d": 0},
                    "HB": {"c": 165, "d": 0}, "HH": {"c": 872, "d": 0},
                    "HE": {"c": 1175, "d": 2}, "MV": {"c": 172, "d": 0},
                    "NI": {"c": 1306, "d": 1}, "NW": {"c": 3545, "d": 6},
                    "RP": {"c": 1053, "d": 2}, "SL": {"c": 187, "d": 0},
                    "SN": {"c": 606, "d": 0}, "ST": {"c": 211, "d": 0},
                    "SH": {"c": 347, "d": 1}, "TH": {"c": 216, "d": 0}
                    }
                }
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
