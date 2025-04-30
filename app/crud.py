from app.database import db

swift_codes_collection = db["swift_codes"]

def get_swift_code(swift_code: str):
    return swift_codes_collection.find_one({"swiftCode": swift_code})

def get_swift_codes_by_country(countryISO2: str):
    return list(swift_codes_collection.find({"countryISO2": countryISO2}))

def create_swift_code(data: dict):
    swift_codes_collection.insert_one(data)
    return True

def delete_swift_code(swift_code: str):
    result = swift_codes_collection.delete_one({"swiftCode": swift_code})
    return result.deleted_count > 0
