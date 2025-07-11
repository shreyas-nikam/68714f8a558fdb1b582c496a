import pytest
from definition_2d0ef8b89d9a4b48853ef11394f22461 import generate_synthetic_control_data
import pandas as pd

def test_generate_synthetic_control_data_positive():
    """Tests that the function returns a Pandas DataFrame with the correct number of rows."""
    num_records = 5
    control_type = ["Preventative", "Detective"]
    key_nonkey = ["Key", "Non-Key"]
    manual_automated = ["Manual", "Automated"]
    risk_level = ["High", "Medium", "Low"]
    implementation_frequency = ["Rare", "Occasional", "Regular", "Frequent"]
    design_quality_rating = ["Poor", "Fair", "Good", "Excellent"]
    df = generate_synthetic_control_data(num_records, control_type, key_nonkey, manual_automated, risk_level, implementation_frequency, design_quality_rating)
    assert isinstance(df, pd.DataFrame)
    assert len(df) == num_records

def test_generate_synthetic_control_data_zero_records():
    """Tests that the function returns an empty Pandas DataFrame when num_records is 0."""
    num_records = 0
    control_type = ["Preventative", "Detective"]
    key_nonkey = ["Key", "Non-Key"]
    manual_automated = ["Manual", "Automated"]
    risk_level = ["High", "Medium", "Low"]
    implementation_frequency = ["Rare", "Occasional", "Regular", "Frequent"]
    design_quality_rating = ["Poor", "Fair", "Good", "Excellent"]
    df = generate_synthetic_control_data(num_records, control_type, key_nonkey, manual_automated, risk_level, implementation_frequency, design_quality_rating)
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 0

def test_generate_synthetic_control_data_invalid_num_records():
    """Tests that the function raises a TypeError when num_records is not an integer."""
    with pytest.raises(TypeError):
        generate_synthetic_control_data("invalid", ["Preventative"], ["Key"], ["Manual"], ["High"], ["Rare"], ["Poor"])

def test_generate_synthetic_control_data_empty_lists():
    """Tests that the function runs with empty category lists"""
    num_records = 5
    control_type = []
    key_nonkey = []
    manual_automated = []
    risk_level = []
    implementation_frequency = []
    design_quality_rating = []
    df = generate_synthetic_control_data(num_records, control_type, key_nonkey, manual_automated, risk_level, implementation_frequency, design_quality_rating)
    assert isinstance(df, pd.DataFrame)
    assert len(df) == num_records

def test_generate_synthetic_control_data_all_single_element_lists():
     """Tests that the function runs with single element category lists"""
     num_records = 5
     control_type = ["Preventative"]
     key_nonkey = ["Key"]
     manual_automated = ["Manual"]
     risk_level = ["High"]
     implementation_frequency = ["Rare"]
     design_quality_rating = ["Poor"]
     df = generate_synthetic_control_data(num_records, control_type, key_nonkey, manual_automated, risk_level, implementation_frequency, design_quality_rating)
     assert isinstance(df, pd.DataFrame)
     assert len(df) == num_records
