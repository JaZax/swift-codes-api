import pytest
from unittest.mock import patch, MagicMock
import pandas as pd
from app.crud import create_swift_code
from app.parser import parse_excel

@pytest.fixture
def mock_excel_data():
    return [
        {
            "ADDRESS": "Cracow",
            "NAME": "Test Bank",
            "COUNTRY ISO2 CODE": "PL",
            "COUNTRY NAME": "POLAND",
            "SWIFT CODE": "ABCDPLP1XXX"
        },
        {
            "ADDRESS": "Cracow",
            "NAME": "Test Bank 2",
            "COUNTRY ISO2 CODE": "PL",
            "COUNTRY NAME": "POLAND",
            "SWIFT CODE": "ABCDPLP1123"
        }
    ]

@pytest.fixture
def mock_excel_file(tmp_path, mock_excel_data):
    file_path = tmp_path / "test.xlsx"
    df = pd.DataFrame(mock_excel_data)
    df.to_excel(file_path, index=False, engine='openpyxl')
    return file_path



def test_parse_excel_success(mock_excel_file, mock_excel_data):
    with patch('app.parser.create_swift_code') as mock_create:
        result = parse_excel(str(mock_excel_file))
        
        assert result["total_records"] == 2
        assert result["success_count"] == 2
        assert result["error_count"] == 0
        assert len(result["errors"]) == 0
        
        # Check that create_swift_code was called with correct data
        assert mock_create.call_count == 2
        for i, call in enumerate(mock_create.call_args_list):
            args, _ = call
            assert args[0]["bankName"] == mock_excel_data[i]["NAME"]
            assert args[0]["swiftCode"] == mock_excel_data[i]["SWIFT CODE"]
            assert args[0]["isHeadquarter"] == mock_excel_data[i]["SWIFT CODE"].endswith("XXX")


def test_parse_excel_file_not_found():
    with patch('app.parser.pd.read_excel') as mock_read:
        mock_read.side_effect = FileNotFoundError("File not found")
        result = parse_excel("nonexistent.xlsx")
        
        assert result is None


def test_parse_excel_row_errors(mock_excel_file):
    bad_data = {
        "ADDRESS": None,
        "NAME": None,
        "COUNTRY ISO2 CODE": "XX",
        "COUNTRY NAME": "Test Country",
        "SWIFT CODE": None
    }
    
    with patch('app.parser.pd.read_excel') as mock_read:
        # return a DataFrame with one good and one bad row
        mock_read.return_value = pd.DataFrame([
            {
            "ADDRESS": "Cracow",
            "NAME": "Test Bank 2",
            "COUNTRY ISO2 CODE": "PL",
            "COUNTRY NAME": "POLAND",
            "SWIFT CODE": "ABCDPLP1123"
            },
            bad_data
        ])
        
        result = parse_excel(str(mock_excel_file))
        
        assert result["total_records"] == 2
        assert result["success_count"] == 1
        assert result["error_count"] == 1
        assert len(result["errors"]) == 1
        assert "Error in row 2" in result["errors"][0]


def test_country_code_conversion(mock_excel_file):
    with patch('app.parser.pd.read_excel') as mock_read:
        mock_read.return_value = pd.DataFrame([
            {
                "ADDRESS": "Old Town",
                "NAME": "Test Bank",
                "COUNTRY ISO2 CODE": "pl",  # lowercase
                "COUNTRY NAME": "poland",   # lowercase
                "SWIFT CODE": "ABCDPLP1XXX"
            }
        ])
        
        with patch('app.parser.create_swift_code') as mock_create:
            parse_excel(str(mock_excel_file))
            
            args, _ = mock_create.call_args
            assert args[0]["countryISO2"] == "PL"
            assert args[0]["countryName"] == "POLAND"


def test_headquarter_detection(mock_excel_file):
    with patch('app.parser.pd.read_excel') as mock_read:
        mock_read.return_value = pd.DataFrame([
            {
            "ADDRESS": "Cracow",
            "NAME": "Test Bank",
            "COUNTRY ISO2 CODE": "PL",
            "COUNTRY NAME": "POLAND",
            "SWIFT CODE": "ABCDPLP1XXX"
            },
            {
            "ADDRESS": "Cracow",
            "NAME": "Test Bank 2",
            "COUNTRY ISO2 CODE": "PL",
            "COUNTRY NAME": "POLAND",
            "SWIFT CODE": "ABCDPLP1123"
            }
        ])
        
        with patch('app.parser.create_swift_code') as mock_create:
            parse_excel(str(mock_excel_file))
            
            calls = mock_create.call_args_list
            assert calls[0][0][0]["isHeadquarter"] is True
            assert calls[1][0][0]["isHeadquarter"] is False


def test_empty_excel_file(mock_excel_file):
    with patch('app.parser.pd.read_excel') as mock_read:
        mock_read.return_value = pd.DataFrame()
        
        result = parse_excel(str(mock_excel_file))
        
        assert result["total_records"] == 0
        assert result["success_count"] == 0
        assert result["error_count"] == 0