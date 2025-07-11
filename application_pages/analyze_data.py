
import streamlit as st
import pandas as pd
import plotly.express as px
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
        "Control_ID": [f"C{i+1}" for i in range(num_records)] # Added Control_ID for validation
    }
    return pd.DataFrame(data)

def load_control_data(file_path, generate_synthetic):
    """Loads control data from a file or generates synthetic data."""
    if file_path:
        try:
            df = pd.read_csv(file_path)
            return df
        except FileNotFoundError:
            st.error(f"File not found: {file_path}")
            return None
        except pd.errors.EmptyDataError:
            st.warning("Uploaded file is empty.")
            return pd.DataFrame()
        except Exception as e:
            st.error(f"Error loading file: {e}")
            return None
    elif generate_synthetic:
        control_types = ["Preventative", "Detective"]
        key_nonkey_options = ["Key", "Non-Key"]
        manual_automated_options = ["Manual", "Automated"]
        risk_level_options = ["High", "Medium", "Low"]
        implementation_frequency_range = [1, 2, 3, 4, 5]
        design_quality_rating_range = [1, 2, 3, 4, 5]

        num_records = st.slider("Number of records", min_value=5, max_value=1000, value=100, help="Number of synthetic control records to generate. Adjust for performance.")
        df = generate_synthetic_control_data(num_records, control_types, key_nonkey_options, manual_automated_options, risk_level_options, implementation_frequency_range, design_quality_rating_range)
        return df
    else:
        st.error("Please upload a file or generate synthetic data.")
        return None

def validate_and_preprocess_data(df):
    """Validates and preprocesses the control data."""
    if df is None:
        return None

    required_columns = ['Control_Type', 'Key_NonKey', 'Manual_Automated', 'Risk_Level',
                        'Implementation_Frequency', 'Design_Quality_Rating', 'Control_ID']
    for col in required_columns:
        if col not in df.columns:
            st.error(f"Column '{col}' is missing.")
            return None

    for col in ['Control_Type', 'Key_NonKey', 'Manual_Automated', 'Risk_Level', 'Control_ID']:
        if not df[col].apply(lambda x: isinstance(x, str)).all():
            st.error(f"Column '{col}' must contain strings.")
            return None

    for col in ['Implementation_Frequency', 'Design_Quality_Rating']:
        df[col] = pd.to_numeric(df[col], errors='coerce')
        if df[col].isnull().any() or not pd.api.types.is_numeric_dtype(df[col]):
            st.error(f"Column '{col}' must contain numbers.")
            return None

    if df.isnull().any().any():
        critical_fields_for_null_check = [col for col in required_columns if col != 'Control_ID']
        if df[critical_fields_for_null_check].isnull().any().any():
            st.error("DataFrame contains missing values in critical columns.")
            return None

    if 'Control_ID' in df.columns and df['Control_ID'].duplicated().any():
        st.error("Control_ID contains duplicate values.")
        return None

    return df

def calculate_control_quality_score(control_type, key_nonkey, manual_automated, implementation_quality_rating):
    """Calculates the Control Quality Score based on control attributes and implementation quality."""

    if control_type not in ("Preventative", "Detective"):
        raise ValueError("Invalid control type")
    if key_nonkey not in ("Key", "Non-Key"):
        raise ValueError("Invalid key/non-key type")
    if manual_automated not in ("Manual", "Automated"):
        raise ValueError("Invalid manual/automated type")
    if not isinstance(implementation_quality_rating, (int, float)) or not (1 <= implementation_quality_rating <= 5):
        raise ValueError("Implementation quality rating must be an integer or float between 1 and 5.")


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

    valid_control_types = ["Preventative", "Detective"]
    valid_key_nonkey = ["Key", "Non-Key"]
    valid_manual_automated = ["Manual", "Automated"]
    valid_risk_levels = ["High", "Medium", "Low"]

    if control_type not in valid_control_types:
        raise ValueError(f"Invalid control type: {control_type}. Must be one of {valid_control_types}")
    if key_nonkey not in valid_key_nonkey:
        raise ValueError(f"Invalid key_nonkey: {key_nonkey}. Must be one of {valid_key_nonkey}")
    if manual_automated not in valid_manual_automated:
        raise ValueError(f"Invalid manual_automated: {manual_automated}. Must be one of {valid_manual_automated}")
    if risk_level not in valid_risk_levels:
        raise ValueError(f"Invalid risk_level: {risk_level}. Must be one of {valid_risk_levels}")

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

def run_analyze_data():
    st.header("Analyze Control Data")

    uploaded_file = st.file_uploader("Upload your control data (CSV format)")
    generate_synthetic = st.checkbox("Generate synthetic data instead")

    df = load_control_data(uploaded_file, generate_synthetic)

    if df is not None:
        df = validate_and_preprocess_data(df)

    if df is not None and not df.empty:
        st.subheader("Data Table")
        st.dataframe(df)

        st.subheader("Summary Statistics")
        st.write(df.describe())
        for col in df.select_dtypes(include='object'):
            st.write(f"Value counts for column '{col}':")
            st.write(df[col].value_counts())

        # Calculate Control Quality Score
        try:
            df['Control_Quality_Score'] = df.apply(lambda row: calculate_control_quality_score(row['Control_Type'], row['Key_NonKey'], row['Manual_Automated'], row['Implementation_Frequency']), axis=1)
        except Exception as e:
            st.error(f"Error calculating Control Quality Score: {e}")

        st.subheader("Visualizations")
        try:
            fig_scatter = px.scatter(df, x="Implementation_Frequency", y="Design_Quality_Rating", color="Control_Type", hover_data=["Control_ID", "Control_Quality_Score"],
                                    title="Relationship between Implementation Frequency and Design Quality")
            fig_scatter.update_layout(xaxis_title="Implementation Frequency (1-5)", yaxis_title="Design Quality Rating (1-5)")
            st.plotly_chart(fig_scatter)

            # Bar chart of average Control Quality Score by Control Type
            df_grouped = df.groupby("Control_Type")["Control_Quality_Score"].mean().reset_index()
            fig_bar = px.bar(df_grouped, x="Control_Type", y="Control_Quality_Score", title="Average Control Quality Score by Control Type")
            st.plotly_chart(fig_bar)
        except Exception as e:
            st.error(f"Error creating visualizations: {e}")
