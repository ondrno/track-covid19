import json
import responses
import pathlib
from cov19.collect import UnitedKingdom


base_path = pathlib.Path(__file__).parent.parent


@responses.activate
def test_get_data_returns_values():
    uk = UnitedKingdom()
    with open("{}/res/uk_fallzahlen.html".format(base_path)) as f:
        body = f.read()
        responses.add(responses.GET, uk.url, body=body, status=200)
        raw_data = uk.get_cov19_data()
        data = json.loads(raw_data)

        assert data['c'] >= 93873
        assert data['d'] >= 12107
        assert data['country'] == "UK"
