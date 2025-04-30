from app.database import db

swift_codes_collection = db["swift_codes"]

def get_swift_code(swift_code: str):
    record = swift_codes_collection.find_one({"swiftCode": swift_code})

    if not record:
        return None

    # If it's a headquarter, find all matching branches
    if record.get("isHeadquarter"):
        base_code = swift_code[:8]
        branches = list(swift_codes_collection.find({
            "swiftCode": {"$regex": f"^{base_code}(?!XXX)"}
        }))
        record["branches"] = branches

    return record

def get_swift_codes_by_country(countryISO2: str):
    return list(swift_codes_collection.find({"countryISO2": countryISO2}))

def create_swift_code(data: dict):
    swift_codes_collection.insert_one(data)
    return True

def delete_swift_code(swift_code: str):
    result = swift_codes_collection.delete_one({"swiftCode": swift_code})
    return result.deleted_count > 0


