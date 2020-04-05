import json
import responses
import pathlib
from cov19.collect import Germany


base_path = pathlib.Path(__file__).parent.parent


@responses.activate
def test_get_data_returns_values():
    expected = {"country": "DE", "c": 91714, "d": 1342,
                "provinces": {
                    "BW": {"c": 18614, "d": 367}, "BY": {"c": 23846, "d": 396},
                    "BE": {"c": 3613, "d": 24}, "BB": {"c": 1305, "d": 17},
                    "HB": {"c": 394, "d": 6}, "HH": {"c": 2945, "d": 19},
                    "HE": {"c": 4575, "d": 56}, "MV": {"c": 523, "d": 5},
                    "NI": {"c": 5712, "d": 89}, "NW": {"c": 18735, "d": 245},
                    "RP": {"c": 3663, "d": 32}, "SL": {"c": 1358, "d": 14},
                    "SN": {"c": 2741, "d": 32}, "ST": {"c": 919, "d": 12},
                    "SH": {"c": 1631, "d": 18}, "TH": {"c": 1140, "d": 10}
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
