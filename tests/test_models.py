import pytest
from app.models import SwiftCodeCreateRequest
from pydantic import ValidationError

def test_invalid_swift_code():
    with pytest.raises(ValidationError) as exc:
        SwiftCodeCreateRequest(
            address="Cracow",
            bankName="Test Bank",
            countryISO2="PL",
            countryName="POLAND",
            isHeadquarter=True,
            swiftCode="INVALID"
        )
    assert "Invalid SWIFT/BIC code" in str(exc.value)

def test_invalid_country_iso2():
    with pytest.raises(ValidationError) as exc:
        SwiftCodeCreateRequest(
            address="Cracow",
            bankName="Test Bank",
            countryISO2="POL",
            countryName="POLAND",
            isHeadquarter=True,
            swiftCode="ABCDPLP1XXX"
        )
    assert "Invalid ISO2 country code" in str(exc.value)

def test_mismatched_country_and_iso2():
    with pytest.raises(ValidationError) as exc:
        SwiftCodeCreateRequest(
            address="Cracow",
            bankName="Test Bank",
            countryISO2="DE",
            countryName="POLAND",
            isHeadquarter=True,
            swiftCode="ABCDPLP1XXX"
        )
    assert "Mismatch" in str(exc.value)