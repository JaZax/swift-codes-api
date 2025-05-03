import pytest
from pymongo import MongoClient

@pytest.fixture(scope="module")
def real_db_connection():
    test_client = MongoClient("mongodb://mongodb:27017")
    test_db = test_client["test_swift_codes_db"]
    yield test_db
    test_client.drop_database("test_swift_codes_db")

def test_real_connection(real_db_connection):
    collection = real_db_connection["test_collection"]
    
    test_data = {"_id": "test1", "value": ":)"}
    collection.insert_one(test_data)
    
    retrieved = collection.find_one({"_id": "test1"})
    assert retrieved["value"] == ":)"