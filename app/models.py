from pydantic import BaseModel, field_validator, model_validator
from typing import List, Optional
from schwifty import BIC
import pycountry

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

    @field_validator("swiftCode")
    def validate_swift_code(cls, v):
        try:
            bic = BIC(v)
            return bic
        except Exception:
            raise ValueError("Invalid SWIFT/BIC code")
        
    @field_validator("countryISO2")
    def validate_iso2(cls, v):
        v = v.upper()
        if not pycountry.countries.get(alpha_2=v):
            raise ValueError("Invalid ISO2 country code")
        return v
    
    @field_validator('countryName')
    def normalize_country_name(cls, v):
        return v.upper()
    
    # validate if ISO2 code matches country name
    @model_validator(mode="after")
    def check_country_match(self) -> "SwiftCodeCreateRequest":
        country = pycountry.countries.get(alpha_2=self.countryISO2)
        if country and country.name.lower() != self.countryName.lower():
            raise ValueError(
                f"Mismatch: {self.countryISO2} is not {self.countryName} (expected: {country.name})"
            )
        return self

class MessageResponse(BaseModel):
    message: str
