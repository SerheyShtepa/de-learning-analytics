import pytest
from de_learning_analytics.ingest import parse_duration, parse_date, normalize_activity


def test_parse_duration():
    assert parse_duration("15") == 15


def test_parse_duration_zero():
    with pytest.raises(ValueError):
        parse_duration("0")


def test_normalize_activity():
    assert normalize_activity(" Audio ") == "audio"


def test_normalize_activity_walking():
    with pytest.raises(ValueError):
        normalize_activity("walking")


def test_parse_date():
    assert parse_date("2025-12-15") == "2025-12-15"


def test_parse_date_invalid():
    with pytest.raises(ValueError):
        parse_date("2025-13-47")
