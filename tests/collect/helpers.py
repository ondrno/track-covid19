from cov19.collect import DataCollector


def assert_if_provinces_have_no_cases_and_deaths(country: DataCollector, data: dict):
    """Check if the data contains all required provinces and that each province has an entry for 'cases' and 'deaths'.
    Assert if not."""
    for p, p_info in country.provinces.items():
        short_name = p_info['short_name']
        assert short_name in data['provinces'], "Could not find province '{} ({})'".format(p, short_name)

        assert 'c' in data['provinces'][short_name], \
            "Could not find 'cases' for province '{} ({})'".format(p, short_name)
        cases = data['provinces'][short_name]['c']
        assert cases > 0, "Invalid number for 'cases' for province '{} ({})'".format(p, short_name)

        assert 'd' in data['provinces'][short_name], \
            "Could not find 'deaths' for province '{} ({})'".format(p, short_name)
        deaths = data['provinces'][short_name]['d']
        assert deaths > 0, "Invalid number for 'deaths' for province '{} ({})'".format(p, short_name)


def assert_if_province_data_is_equal(country: DataCollector, data: dict):
    """Check if the province data is unique among all other provinces, i.e. compare every data set with all others
    and assert if the same data is found twice. This is very unlikely and therefore must not happen."""
    for p, p_info in country.provinces.items():
        short_name = p_info['short_name']

        needle = data['provinces'][short_name]
        for province in data['provinces']:
            if short_name == province:
                continue
            assert needle != data['provinces'][province], \
                "Found data twice ({}): {} vs. {}".format(short_name, needle, data['provinces'][province])
