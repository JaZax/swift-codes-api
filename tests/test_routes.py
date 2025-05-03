import pytest
import requests

BASE_URL = "http://localhost:8080/v1/swift-codes"

swift_payload_hq = {
    "address": "Cracow",
    "bankName": "uwu bank",
    "countryISO2": "PL",
    "countryName": "POLAND",
    "isHeadquarter": True,
    "swiftCode": "ABCDPLP1XXX"
}

swift_payload_branch = {
    "address": "Cracow",
    "bankName": "uwu bank branch",
    "countryISO2": "PL",
    "countryName": "POLAND",
    "isHeadquarter": False,
    "swiftCode": "ABCDPLP1123"
}

@pytest.fixture(scope="module", autouse=True)
def clean_test_swift_codes():
    # Before tests
    requests.delete(BASE_URL + "/ABCDPLP1XXX")
    requests.delete(BASE_URL + "/ABCDPLP1123")
    requests.delete(BASE_URL + "/AACDPLP1122")
    requests.delete(BASE_URL + "/AACBPLP1122")
    yield
    # After tests
    requests.delete(BASE_URL + "/ABCDPLP1XXX")
    requests.delete(BASE_URL + "/ABCDPLP1123")
    requests.delete(BASE_URL + "/AACDPLP1122")
    requests.delete(BASE_URL + "/AACBPLP1122")

class TestCreateSwiftCodes:
    def test_add_hq_swift_code(self):
        res = requests.post(BASE_URL + "/", json=swift_payload_hq)
        assert res.status_code == 200
        assert res.json()["message"] == "SWIFT code added successfully"

    def test_add_branch_swift_code(self):
        res = requests.post(BASE_URL + "/", json=swift_payload_branch)
        assert res.status_code == 200

    def test_add_duplicate_swift_code(self):
        res = requests.post(BASE_URL + "/", json=swift_payload_hq)
        assert res.status_code == 409
        assert res.json()["detail"] == "SWIFT code already exists"

    def test_add_invalid_countries_swift_code(self):
        payload = {
            "address": "Warsaw",
            "bankName": "owo bank branch",
            "countryISO2": "PL",
            "countryName": "germany",
            "isHeadquarter": False,
            "swiftCode": "AACDPLP1122"
        }
        res = requests.post(BASE_URL + "/", json=payload)
        assert res.status_code == 422
        assert res.json()['detail'][0]['msg'] == "Value error, Mismatch: PL is not GERMANY (expected: Poland)"

    def test_add_invalid_swift_code(self):
        payload = {
            "address": "Warsaw",
            "bankName": "owo bank branch",
            "countryISO2": "PL",
            "countryName": "POLAND",
            "isHeadquarter": False,
            "swiftCode": "AAAAAAA"
        }
        res = requests.post(BASE_URL + "/", json=payload)
        assert res.status_code == 422
        assert res.json()['detail'][0]['msg'] == "Value error, Invalid SWIFT/BIC code"

    def test_add_invalid_iso2_code(self):
        payload = {
            "address": "Warsaw",
            "bankName": "owo bank branch",
            "countryISO2": "XX",
            "countryName": "POLAND",
            "isHeadquarter": False,
            "swiftCode": "AACDPLP1122"
        }
        res = requests.post(BASE_URL + "/", json=payload)
        assert res.status_code == 422
        assert res.json()['detail'][0]['msg'] == "Value error, Invalid ISO2 country code"

class TestGetSwiftCodes:
    def test_get_hq_swift_code(self):
        res = requests.get(BASE_URL + f"/{swift_payload_hq['swiftCode']}")
        assert res.status_code == 200
        assert res.json()["isHeadquarter"] is True
        assert "branches" in res.json()

    def test_get_branch_swift_code(self):
        res = requests.get(BASE_URL + f"/{swift_payload_branch['swiftCode']}")
        assert res.status_code == 200
        assert res.json()["isHeadquarter"] is False
        assert "branches" not in res.json()

    def test_get_invalid_swift_code(self):
        res = requests.get(BASE_URL + "/INVALIDCODE")
        assert res.status_code == 404
        assert res.json()["detail"] == "SWIFT code not found"

class TestCountrySwiftCodes:
    def test_get_country_swift_codes(self):
        res = requests.get(BASE_URL + "/country/PL")
        assert res.status_code == 200
        assert res.json()["countryISO2"] == "PL"
        assert "swiftCodes" in res.json()

    def test_get_invalid_country(self):
        res = requests.get(BASE_URL + "/country/XX")
        assert res.status_code == 400
        assert res.json()["detail"] == "Invalid ISO2 country code"

class TestDeleteSwiftCodes:
    def test_delete_swift_code(self):
        payload = {
            "address": "Warsaw",
            "bankName": "owo bank branch",
            "countryISO2": "PL",
            "countryName": "POLAND",
            "isHeadquarter": False,
            "swiftCode": "AACBPLP1122"
        }
        res = requests.post(BASE_URL + "/", json=payload)
        assert res.status_code == 200

        res = requests.delete(BASE_URL + f"/{swift_payload_hq['swiftCode']}")
        assert res.status_code == 200
        assert res.json()["message"] == "SWIFT code deleted successfully"

    def test_delete_non_existing_swift_code(self):
        res = requests.delete(BASE_URL + "/DOESNOTEXIST")
        assert res.status_code == 404
        assert res.json()["detail"] == "SWIFT code not found"
