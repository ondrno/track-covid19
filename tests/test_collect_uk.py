import json
import responses
import pathlib
from cov19 import UnitedKingdom


base_path = pathlib.Path(__file__).parent


@responses.activate
def test_get_data_returns_values():
    uk = UnitedKingdom()
    uk.url = "{}/res/uk_fallzahlen.xlsx".format(base_path)
    data = uk.get_cov19_data()
    assert data == json.dumps({"country": "UK", 'c': 797, 'd': 10})
