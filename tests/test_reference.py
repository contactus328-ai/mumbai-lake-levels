from lakelevels import reference


def test_seven_lakes_listed():
    lakes = reference.get_lakes()
    assert len(lakes) == 7
    names = {lake["name"] for lake in lakes}
    assert "Tulsi" in names
    assert "Vihar" in names


def test_water_balance_has_expected_keys():
    balance = reference.get_water_balance()
    assert "daily_demand_mld" in balance
    assert "daily_supply_mld" in balance


def test_usage_breakdown_sums_to_100():
    usage = reference.get_usage_breakdown()
    total = sum(v for k, v in usage.items() if isinstance(v, (int, float)))
    assert total == 100
