from pydantic import BaseModel
from typing import List, Optional

class Branch(BaseModel):
    address: str
    bankName: str
    countryISO2: str
    isHeadquarter: bool
    swiftCode: str

class SwiftCodeResponse(BaseModel):
    address: str
    bankName: str
    countryISO2: str
    countryName: str
    isHeadquarter: bool
    swiftCode: str
    branches: Optional[List[Branch]] = None

class CountrySwiftCodesResponse(BaseModel):
    countryISO2: str
    countryName: str
    swiftCodes: List[Branch]

class SwiftCodeCreateRequest(BaseModel):
    address: str
    bankName: str
    countryISO2: str
    countryName: str
    isHeadquarter: bool
    swiftCode: str

class MessageResponse(BaseModel):
    message: str
