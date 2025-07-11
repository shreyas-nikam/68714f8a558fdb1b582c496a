import pytest
import pandas as pd
from definition_a74c8bc21162478e8de7d7fbea48e295 import validate_and_preprocess_data


def test_validate_and_preprocess_data_valid_df():
    data = {'Control_Type': ['Preventative'], 'Key_NonKey': ['Key'], 'Manual_Automated': ['Automated'],
            'Risk_Level': ['High'], 'Implementation_Frequency': [10], 'Design_Quality_Rating': [5], 'Control_ID': ['C1']}
    df = pd.DataFrame(data)
    cleaned_df = validate_and_preprocess_data(df.copy())
    assert cleaned_df.equals(df)


def test_validate_and_preprocess_data_missing_column():
    data = {'Key_NonKey': ['Key'], 'Manual_Automated': ['Automated'],
            'Risk_Level': ['High'], 'Implementation_Frequency': [10], 'Design_Quality_Rating': [5], 'Control_ID': ['C1']}
    df = pd.DataFrame(data)
    with pytest.raises(KeyError):
        validate_and_preprocess_data(df.copy())


def test_validate_and_preprocess_data_invalid_data_type():
    data = {'Control_Type': [123], 'Key_NonKey': ['Key'], 'Manual_Automated': ['Automated'],
            'Risk_Level': ['High'], 'Implementation_Frequency': [10], 'Design_Quality_Rating': [5], 'Control_ID': ['C1']}
    df = pd.DataFrame(data)
    with pytest.raises(TypeError):
        validate_and_preprocess_data(df.copy())


def test_validate_and_preprocess_data_missing_values():
    data = {'Control_Type': ['Preventative', None], 'Key_NonKey': ['Key', 'Non-Key'], 'Manual_Automated': ['Automated', 'Manual'],
            'Risk_Level': ['High', 'Medium'], 'Implementation_Frequency': [10, 5], 'Design_Quality_Rating': [5, 2], 'Control_ID': ['C1', 'C2']}
    df = pd.DataFrame(data)
    with pytest.raises(ValueError):
        validate_and_preprocess_data(df.copy())


def test_validate_and_preprocess_data_duplicate_control_id():
    data = {'Control_Type': ['Preventative', 'Detective'], 'Key_NonKey': ['Key', 'Non-Key'], 'Manual_Automated': ['Automated', 'Manual'],
            'Risk_Level': ['High', 'Medium'], 'Implementation_Frequency': [10, 5], 'Design_Quality_Rating': [5, 2], 'Control_ID': ['C1', 'C1']}
    df = pd.DataFrame(data)
    with pytest.raises(ValueError):
        validate_and_preprocess_data(df.copy())
