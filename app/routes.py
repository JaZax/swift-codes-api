from fastapi import APIRouter, HTTPException
import pycountry

from app.models import SwiftCodeResponse, CountrySwiftCodesResponse, SwiftCodeCreateRequest, MessageResponse
from app import crud

router = APIRouter()

@router.get(
    "/{swift_code}",
    summary="Get SWIFT code details",
    description="Retrieve information for a specific SWIFT code.",
    response_model=SwiftCodeResponse,
    response_model_exclude_none=True, # when isHeadquarter is false, then branches = none
    responses={
        404: {"description": "SWIFT code not found"},
    }
)
def get_single_swift_code(swift_code: str):
    swift_data = crud.get_swift_code(swift_code)
    if not swift_data:
        raise HTTPException(status_code=404, detail="SWIFT code not found")
        
    return SwiftCodeResponse(**swift_data)


@router.get(
        "/country/{countryISO2}", 
        summary="List SWIFT codes by country",
        description="Fetch all SWIFT codes associated with a given ISO2 country code.",
        response_model=CountrySwiftCodesResponse,
        responses={
        400: {"description": "Invalid ISO2 country code"},
        404: {"description": "No SWIFT codes found for country"},
    })
def get_country_swift_codes(countryISO2: str):
    countryISO2 = countryISO2.upper()
    if not pycountry.countries.get(alpha_2=countryISO2):
        raise HTTPException(status_code=400, detail="Invalid ISO2 country code")

    swifts = crud.get_swift_codes_by_country(countryISO2)
    if not swifts:
        raise HTTPException(status_code=404, detail="No SWIFT codes found for country")
    
    return CountrySwiftCodesResponse(
        countryISO2=countryISO2,
        countryName=swifts[0]["countryName"],
        swiftCodes=swifts
    )


@router.post(
    "/",
    summary="Add a new SWIFT code",
    description="Create a new SWIFT code entry. Validates input and ensures the code does not already exist in the system.",
    response_model=MessageResponse,
    responses={
        409: {"description": "SWIFT code already exists"},
    }
)
def add_swift_code(swift_request: SwiftCodeCreateRequest):
    swift_code = swift_request.swiftCode

    if crud.get_swift_code(swift_code):
        raise HTTPException(status_code=409, detail="SWIFT code already exists")

    crud.create_swift_code(swift_request.model_dump())

    return MessageResponse(message="SWIFT code added successfully")


@router.delete(
    "/{swift_code}",
    summary="Delete a SWIFT code",
    description="Delete a SWIFT code from the database. Returns a success message if the code was found and removed.",
    response_model=MessageResponse,
    responses={
        404: {"description": "SWIFT code not found"},
    }
)
def delete_swift_code(swift_code: str):
    deleted = crud.delete_swift_code(swift_code)
    if not deleted:
        raise HTTPException(status_code=404, detail="SWIFT code not found")
    
    return MessageResponse(message="SWIFT code deleted successfully")
