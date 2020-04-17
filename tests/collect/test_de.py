import json
import responses
import pathlib
from cov19.collect import Germany
from .helpers import assert_if_province_data_is_equal, assert_if_provinces_have_no_cases_and_deaths


base_path = pathlib.Path(__file__).parent.parent


@responses.activate
def test_get_data_returns_values():
    de = Germany()
    with open("{}/res/de_fallzahlen.html".format(base_path)) as f:
        body = f.read()
        responses.add(responses.GET, de.url, body=body, status=200)
        raw_data = de.get_cov19_data()
        data = json.loads(raw_data)

        assert data['country'] == "DE"
        assert 'c' in data, "Could not find 'cases'"
        assert data['c'] >= 91714, 'Invalid number for cases in DE'.format(91714, data['c'])

        assert 'd' in data, "Could not find 'deaths'"
        assert data['d'] >= 1342, 'Invalid number for deaths in DE'.format(1342, data['d'])

        assert_if_provinces_have_no_cases_and_deaths(de, data)
        assert_if_province_data_is_equal(de, data)
