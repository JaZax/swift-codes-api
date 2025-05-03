import pandas as pd

from app.crud import create_swift_code
from app.models import SwiftCodeCreateRequest

def parse_excel(file_path: str):
    try:
        df = pd.read_excel(file_path, engine='openpyxl')
        print(f"✔ Successfully loaded Excel file with {len(df)} records")
    except Exception as e:
        print(f"✖ Failed to load Excel file: {str(e)}")
        return
    
    if df.empty:
        print("✖ Empty Excel file - no records to process")
        return {
            "total_records": 0,
            "success_count": 0,
            "error_count": 0,
            "errors": []
        }
    
    required_columns = {
        "ADDRESS", "NAME", "COUNTRY ISO2 CODE", 
        "COUNTRY NAME", "SWIFT CODE"
    }

    missing_columns = required_columns - set(df.columns)

    if missing_columns:
        print(f"✖ Missing required columns: {missing_columns}")
        return {
            "total_records": 0,
            "success_count": 0,
            "error_count": 0,
            "errors": [f"Missing columns: {missing_columns}"]
        }

    df['COUNTRY ISO2 CODE'] = df['COUNTRY ISO2 CODE'].str.upper()
    df['COUNTRY NAME'] = df['COUNTRY NAME'].str.upper()
    df['IS HEADQUARTER'] = df['SWIFT CODE'].str.endswith('XXX')

    success_count = 0
    error_count = 0
    errors = []

    for index, row in df.iterrows():
        try:
            data = SwiftCodeCreateRequest(
                address=row['ADDRESS'],
                bankName=row['NAME'],
                countryISO2=row['COUNTRY ISO2 CODE'],
                countryName=row['COUNTRY NAME'],
                isHeadquarter=row['IS HEADQUARTER'],
                swiftCode=row['SWIFT CODE']
            )
            create_swift_code(data.model_dump())
            success_count += 1
        except Exception as e:
            error_count += 1
            error_msg = f"\n✖ Error in row {index+1} ({row.get('SWIFT CODE', 'N/A')}): {str(e)}"
            errors.append(error_msg)
            print(error_msg)

    print("Parsing Summary:")
    print(f"Total records: {len(df)}")
    print(f"Successfully processed: {success_count}")
    print(f"Failed: {error_count}")
    
    if errors:
        print("\nError Details:")
        for error in errors:
            print(f"\n- {error}")

    return {
        "total_records": len(df),
        "success_count": success_count,
        "error_count": error_count,
        "errors": errors
    }
