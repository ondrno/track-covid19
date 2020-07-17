import json
import responses
import pathlib
from cov19.collect import Switzerland


base_path = pathlib.Path(__file__).parent.parent


@responses.activate
def test_get_data_returns_values():
    ch = Switzerland()
    with open("{}/res/ch_fallzahlen.html".format(base_path)) as f:
        body = f.read()
        responses.add(responses.GET, ch.url, body=body, status=200)
        raw_data = ch.get_cov19_data()

        data = json.loads(raw_data)
        assert data['c'] >= 33382
        assert data['d'] >= 1688
