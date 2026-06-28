from backend.schemas.maintenance import MaintenanceRecord


def test_project():
    assert True


def test_maintenance_record_defaults_and_values():
    record = MaintenanceRecord(asset="Pump P-204", issue="High bearing temperature")

    assert record.asset == "Pump P-204"
    assert record.issue == "High bearing temperature"
    assert record.priority == ""
    assert record.operator == ""
    assert record.recommendation == ""
