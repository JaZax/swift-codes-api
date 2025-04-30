from fastapi import APIRouter, HTTPException
from app.models import SwiftCodeResponse, CountrySwiftCodesResponse, SwiftCodeCreateRequest, MessageResponse
from app import crud

router = APIRouter()

@router.get("/{swift_code}", response_model=SwiftCodeResponse)
def get_single_swift_code(swift_code: str):
    swift = crud.get_swift_code(swift_code)
    if not swift:
        raise HTTPException(status_code=404, detail="SWIFT code not found")
    return swift

@router.get("/country/{countryISO2}", response_model=CountrySwiftCodesResponse)
def get_country_swift_codes(countryISO2: str):
    swifts = crud.get_swift_codes_by_country(countryISO2)
    if not swifts:
        raise HTTPException(status_code=404, detail="No SWIFT codes found for country")
    return {
        "countryISO2": countryISO2,
        "countryName": swifts[0]["countryName"],
        "swiftCodes": swifts
    }

@router.post("/", response_model=MessageResponse)
def add_swift_code(swift_request: SwiftCodeCreateRequest):
    crud.create_swift_code(swift_request.dict())
    return {"message": "SWIFT code added successfully"}

@router.delete("/{swift_code}", response_model=MessageResponse)
def delete_swift(swift_code: str):
    deleted = crud.delete_swift_code(swift_code)
    if not deleted:
        raise HTTPException(status_code=404, detail="SWIFT code not found")
    return {"message": "SWIFT code deleted successfully"}
