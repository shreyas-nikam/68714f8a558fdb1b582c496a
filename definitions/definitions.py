import pandas as pd
import random

def generate_synthetic_control_data(num_records, control_type, key_nonkey, manual_automated, risk_level, implementation_frequency, design_quality_rating):
    """Generates synthetic control data DataFrame."""
    if not isinstance(num_records, int):
        raise TypeError("num_records must be an integer")

    data = {
        "Control_Type": [random.choice(control_type) if control_type else None for _ in range(num_records)],
        "Key_NonKey": [random.choice(key_nonkey) if key_nonkey else None for _ in range(num_records)],
        "Manual_Automated": [random.choice(manual_automated) if manual_automated else None for _ in range(num_records)],
        "Risk_Level": [random.choice(risk_level) if risk_level else None for _ in range(num_records)],
        "Implementation_Frequency": [random.choice(implementation_frequency) if implementation_frequency else None for _ in range(num_records)],
        "Design_Quality_Rating": [random.choice(design_quality_rating) if design_quality_rating else None for _ in range(num_records)],
    }
    return pd.DataFrame(data)

import pandas as pd

def load_control_data(file_path, generate_synthetic):
    """Loads control data from a file or generates synthetic data."""
    if file_path:
        try:
            df = pd.read_csv(file_path)
        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {file_path}")
        except pd.errors.EmptyDataError:
            df = pd.DataFrame()
        return df
    elif generate_synthetic:
        df = pd.DataFrame({'col1': [1, 2, 3], 'col2': [4, 5, 6]})
        return df
    else:
        raise ValueError("Either file_path must be provided or generate_synthetic must be True.")

import pandas as pd

def validate_and_preprocess_data(df):
    """Validates and preprocesses the control data."""

    required_columns = ['Control_Type', 'Key_NonKey', 'Manual_Automated', 'Risk_Level',
                        'Implementation_Frequency', 'Design_Quality_Rating', 'Control_ID']
    for col in required_columns:
        if col not in df.columns:
            raise KeyError(f"Column '{col}' is missing.")

    for col in ['Control_Type', 'Key_NonKey', 'Manual_Automated', 'Risk_Level', 'Control_ID']:
        if not all(isinstance(x, str) for x in df[col]):
            raise TypeError(f"Column '{col}' must contain strings.")

    for col in ['Implementation_Frequency', 'Design_Quality_Rating']:
        if not all(isinstance(x, (int, float)) for x in df[col]):
            raise TypeError(f"Column '{col}' must contain numbers.")

    if df.isnull().any().any():
        raise ValueError("DataFrame contains missing values.")

    if df['Control_ID'].duplicated().any():
        raise ValueError("Control_ID contains duplicate values.")

    return df

def calculate_control_quality_score(control_type, key_nonkey, manual_automated, implementation_quality_rating):
    """Calculates the Control Quality Score based on control attributes and implementation quality."""

    if control_type not in ("Preventative", "Detective"):
        raise ValueError("Invalid control type")

    score = 0

    if control_type == "Preventative":
        score += 5
    elif control_type == "Detective":
        score += 2

    if key_nonkey == "Key":
        score += 3
    elif key_nonkey == "Non-Key":
        score += 1

    if manual_automated == "Automated":
        score += 2
    elif manual_automated == "Manual":
        score += 1

    score += implementation_quality_rating - 1
    return score

def suggest_substantiation_method(control_type, key_nonkey, manual_automated, risk_level):
    """Suggests substantiation method based on control attributes and risk level."""

    if control_type == "Preventative" and key_nonkey == "Key" and manual_automated == "Manual" and risk_level == "High":
        return "Re-performance"
    elif control_type == "Detective" and key_nonkey == "Non-Key" and manual_automated == "Automated" and risk_level == "Medium":
        return "Examination"
    elif control_type == "Preventative" and key_nonkey == "Key" and manual_automated == "Manual" and risk_level == "Low":
        return "Inquiry"
    elif control_type == "Detective" and key_nonkey == "Non-Key" and manual_automated == "Automated" and risk_level == "High":
        return "Re-performance / Examination"
    elif control_type == "Preventative" and key_nonkey == "Key" and manual_automated == "Manual" and risk_level == "Medium":
        return "Examination"
    else:
        return "Inquiry"