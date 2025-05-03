import mongomock
import pytest

from app import crud

@pytest.fixture(autouse=True)
def mock_db(monkeypatch):
    mock_client = mongomock.MongoClient()
    mock_db = mock_client["test_db"]
    collection = mock_db["swift_codes"]
    monkeypatch.setattr(crud, "swift_codes_collection", collection)
    return collection


def test_create_and_get_swift_code(mock_db):
    data = {
        "swiftCode": "ABCDEF12XXX",
        "countryISO2": "PL",
        "isHeadquarter": True
    }
    crud.create_swift_code(data)
    result = crud.get_swift_code("ABCDEF12XXX")

    assert result is not None
    assert result["swiftCode"] == "ABCDEF12XXX"


def test_get_swift_code_with_branches(mock_db):
    hq = {"swiftCode": "BANKPL33XXX", "countryISO2": "PL", "isHeadquarter": True}
    branch1 = {"swiftCode": "BANKPL33KRK", "countryISO2": "PL", "isHeadquarter": False}
    branch2 = {"swiftCode": "BANKPL33KTW", "countryISO2": "PL", "isHeadquarter": False}
    mock_db.insert_many([hq, branch1, branch2])

    result = crud.get_swift_code("BANKPL33XXX")

    assert result["swiftCode"] == "BANKPL33XXX"
    assert "branches" in result
    assert len(result["branches"]) == 2
    branch_codes = {b["swiftCode"] for b in result["branches"]}
    assert branch_codes == {"BANKPL33KRK", "BANKPL33KTW"}


def test_get_swift_codes_by_country(mock_db):
    mock_db.insert_many([
        {"swiftCode": "FR123", "countryISO2": "FR"},
        {"swiftCode": "FR456", "countryISO2": "FR"},
        {"swiftCode": "DE789", "countryISO2": "DE"}
    ])

    result = crud.get_swift_codes_by_country("FR")

    assert len(result) == 2
    assert all(r["countryISO2"] == "FR" for r in result)


def test_delete_swift_code(mock_db):
    mock_db.insert_one({"swiftCode": "DEL999", "countryISO2": "UK"})

    deleted = crud.delete_swift_code("DEL999")
    after = crud.get_swift_code("DEL999")

    assert deleted is True
    assert after is None
