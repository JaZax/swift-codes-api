## Endpoints

### 1. Retrieve details of a single SWIFT code whether for a headquarters or branches.

**GET**: `/v1/swift-codes/{swift-code}`

Response Structure for headquarter swift code:
```py
{
    "address": string,
    "bankName": string,
    "countryISO2": string,
    "countryName": string,
    "isHeadquarter": bool,
    "swiftCode": string,
    "branches": [
            {
            "address": string,
            "bankName": string,
            "countryISO2": string,
            "isHeadquarter": bool,
            "swiftCode": string
            },
            {
            "address": string,
            "bankName": string,
            "countryISO2": string,
            "isHeadquarter": bool,
            "swiftCode": string
            }, . . .
        ]
}
```

Response Structure for branch swift code: 
```py
{
    "address": string,
    "bankName": string,
    "countryISO2": string,
    "countryName": string,
    "isHeadquarter": bool,
    "swiftCode": string
}
```

---

### 2. Return all SWIFT codes with details for a specific country 
(both headquarters and branches).

**GET**:  `/v1/swift-codes/country/{countryISO2code}`

Response Structure:
```py
{
    "countryISO2": string,
    "countryName": string,
    "swiftCodes": [
        {
            "address": string,
    		 "bankName": string,
    		 "countryISO2": string,
    		 "isHeadquarter": bool,
    		 "swiftCode": string
        },
        {
            "address": string,
    		 "bankName": string,
    		 "countryISO2": string,
    		 "isHeadquarter": bool,
    		 "swiftCode": string
        }, . . .
    ]
}
```

---

### 3. Add new SWIFT code entries to the database for a specific country.

**POST**:  `/v1/swift-codes`

Request Structure :
```py
{
    "address": string,
    "bankName": string,
    "countryISO2": string,
    "countryName": string,
    "isHeadquarter": bool,
    "swiftCode": string,
}
```
Response Structure: 
```py
{
    "message": string,
}
```

---

### 4. Delete swift-code data if swiftCode matches the one in the database.
**DELETE**:  `/v1/swift-codes/{swift-code}`

Response Structure: 
```py
{
    "message": string,
}
```
