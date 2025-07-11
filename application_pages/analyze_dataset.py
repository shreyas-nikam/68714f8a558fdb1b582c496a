
import streamlit as st
import pandas as pd
import random
import plotly.express as px
import plotly.graph_objects as go

# --- Data Generation Function ---
def generate_synthetic_control_data(num_records, control_type, key_nonkey, manual_automated, risk_level, implementation_frequency, design_quality_rating):
    """Generates synthetic control data DataFrame."""
    if not isinstance(num_records, int):
        raise TypeError("num_records must be an integer")

    data = {
        "Control_Type": [random.choice(control_type) for _ in range(num_records)],
        "Key_NonKey": [random.choice(key_nonkey) for _ in range(num_records)],
        "Manual_Automated": [random.choice(manual_automated) for _ in range(num_records)],
        "Risk_Level": [random.choice(risk_level) for _ in range(num_records)],
        "Implementation_Frequency": [random.choice(implementation_frequency) for _ in range(num_records)],
        "Design_Quality_Rating": [random.choice(design_quality_rating) for _ in range(num_records)],
    }
    df = pd.DataFrame(data)
    # Crucial Modification: Add Control_ID for synthetic data
    df['Control_ID'] = [f'C{i+1:04d}' for i in range(len(df))]
    return df

# --- Data Loading Function (Streamlit Adapted) ---
@st.cache_data
def load_control_data_streamlit(file_upload_obj, num_synthetic_records=None):
    """Loads control data from a file or generates synthetic data."""
    df = pd.DataFrame() # Initialize empty DataFrame

    if file_upload_obj is not None:
        try:
            df = pd.read_csv(file_upload_obj)
        except pd.errors.EmptyDataError:
            st.error("Uploaded file is empty. Please upload a valid CSV.")
        except Exception as e:
            st.error(f"Error reading uploaded file: {e}")
    elif num_synthetic_records is not None and num_synthetic_records > 0:
        # Call the comprehensive synthetic data generator
        control_type_opts = ["Preventative", "Detective"]
        key_nonkey_opts = ["Key", "Non-Key"]
        manual_automated_opts = ["Manual", "Automated"]
        risk_level_opts = ["High", "Medium", "Low"]
        implementation_frequency_opts = [1, 2, 3, 4, 5]
        design_quality_rating_opts = [1, 2, 3, 4, 5]

        df = generate_synthetic_control_data(
            num_records=num_synthetic_records,
            control_type=control_type_opts,
            key_nonkey=key_nonkey_opts,
            manual_automated=manual_automated_opts,
            risk_level=risk_level_opts,
            implementation_frequency=implementation_frequency_opts,
            design_quality_rating=design_quality_rating_opts
        )
    return df

# --- Data Validation and Preprocessing Function ---
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
        try:
            df[col] = pd.to_numeric(df[col], errors='coerce')
            if df[col].isnull().any():
                raise TypeError(f"Column '{col}' contains non-numeric values after conversion.")
        except ValueError:
            raise TypeError(f"Column '{col}' must contain numbers.")

    if df.isnull().any().any():
        raise ValueError("DataFrame contains missing values.")

    if df['Control_ID'].duplicated().any():
        raise ValueError("Control_ID contains duplicate values.")

    return df

# --- Control Quality Score Calculation Function ---
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

# --- Control Substantiation Method Suggestion Function ---
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

def run_analyze_dataset():
    st.header("Analyze Control Dataset")

    st.sidebar.subheader("Data Source Selection")
    data_source_option = st.sidebar.radio(
        "Choose Data Source",
        ("Upload CSV File", "Generate Synthetic Data"),
        help="Select whether to upload your own control data or generate a synthetic dataset."
    )

    raw_df = pd.DataFrame()
    num_synthetic_records = None

    if data_source_option == "Upload CSV File":
        uploaded_file = st.sidebar.file_uploader(
            "Upload CSV File",
            type=["csv"],
            help="Upload a CSV file containing control data with columns: Control_Type, Key_NonKey, Manual_Automated, Risk_Level, Implementation_Frequency, Design_Quality_Rating, Control_ID."
        )
        if uploaded_file is not None:
            raw_df = load_control_data_streamlit(uploaded_file)
    else: # Generate Synthetic Data
        num_synthetic_records = st.sidebar.number_input(
            "Number of Synthetic Records",
            min_value=10,
            max_value=1000,
            value=50,
            step=10,
            help="Specify the number of synthetic control records to generate for analysis. A larger number may take slightly longer to process."
        )
        if st.sidebar.button("Generate Data"):
            raw_df = load_control_data_streamlit(None, num_synthetic_records)
            st.success(f"{num_synthetic_records} synthetic records generated.")

    processed_df = pd.DataFrame() # Initialize processed_df

    if not raw_df.empty:
        try:
            processed_df = validate_and_preprocess_data(raw_df.copy()) # Pass a copy
            st.success("Data loaded and validated successfully!")

            # Calculate Control Quality Score
            processed_df['Control_Quality_Score'] = processed_df.apply(
                lambda row: calculate_control_quality_score(
                    row['Control_Type'],
                    row['Key_NonKey'],
                    row['Manual_Automated'],
                    row['Implementation_Frequency'] # Using Implementation_Frequency as the rating input
                ), axis=1
            )
            st.success("Control Quality Scores calculated.")

            # Suggest Substantiation Method
            processed_df['Suggested_Method'] = processed_df.apply(
                lambda row: suggest_substantiation_method(
                    row['Control_Type'],
                    row['Key_NonKey'],
                    row['Manual_Automated'],
                    row['Risk_Level']
                ), axis=1
            )
            st.success("Suggested Substantiation Methods generated.")

            st.subheader("Validated Data Sample:")
            st.dataframe(processed_df.head())

            st.divider()

            st.sidebar.subheader("Dataset Filters")
            all_control_types = processed_df['Control_Type'].unique().tolist()
            all_key_nonkey = processed_df['Key_NonKey'].unique().tolist()
            all_manual_automated = processed_df['Manual_Automated'].unique().tolist()
            all_risk_levels = processed_df['Risk_Level'].unique().tolist()

            selected_control_types = st.sidebar.multiselect("Filter by Control Type", options=all_control_types, default=all_control_types)
            selected_key_nonkey = st.sidebar.multiselect("Filter by Key/Non-Key", options=all_key_nonkey, default=all_key_nonkey)
            selected_manual_automated = st.sidebar.multiselect("Filter by Manual/Automated", options=all_manual_automated, default=all_manual_automated)
            selected_risk_levels = st.sidebar.multiselect("Filter by Risk Level", options=all_risk_levels, default=all_risk_levels)

            min_freq, max_freq = int(processed_df['Implementation_Frequency'].min()), int(processed_df['Implementation_Frequency'].max())
            min_design, max_design = int(processed_df['Design_Quality_Rating'].min()), int(processed_df['Design_Quality_Rating'].max())

            freq_range = st.sidebar.slider("Implementation Frequency Range", min_value=min_freq, max_value=max_freq, value=(min_freq, max_freq))
            design_range = st.sidebar.slider("Design Quality Rating Range", min_value=min_design, max_value=max_design, value=(min_design, max_design))

            filtered_df = processed_df[
                (processed_df['Control_Type'].isin(selected_control_types)) &
                (processed_df['Key_NonKey'].isin(selected_key_nonkey)) &
                (processed_df['Manual_Automated'].isin(selected_manual_automated)) &
                (processed_df['Risk_Level'].isin(selected_risk_levels)) &
                (processed_df['Implementation_Frequency'] >= freq_range[0]) &
                (processed_df['Implementation_Frequency'] <= freq_range[1]) &
                (processed_df['Design_Quality_Rating'] >= design_range[0]) &
                (processed_df['Design_Quality_Rating'] <= design_range[1])
            ]

            st.subheader("Filtered Data:")
            st.dataframe(filtered_df)

            st.divider()

            # --- Visualizations ---
            if not filtered_df.empty:
                st.subheader("Visualizations")

                # Relationship Plot (Scatter Plot)
                st.markdown("### Relationship between Control Attributes and Quality Score")
                fig_scatter = px.scatter(
                    filtered_df,
                    x="Implementation_Frequency",
                    y="Design_Quality_Rating",
                    color="Control_Type",
                    size="Control_Quality_Score",
                    hover_data=[
                        'Control_ID', 'Key_NonKey', 'Manual_Automated', 'Risk_Level',
                        'Control_Quality_Score', 'Suggested_Method'
                    ],
                    title="Control Quality vs. Implementation & Design",
                    labels={
                        "Implementation_Frequency": "Implementation Frequency (Rating 1-5)",
                        "Design_Quality_Rating": "Design Quality Rating (Rating 1-5)",
                        "Control_Type": "Control Type"
                    },
                    color_discrete_sequence=px.colors.qualitative.Plotly # Color-blind friendly palette
                )
                fig_scatter.update_layout(
                    xaxis_title="Implementation Frequency (Rating 1-5)",
                    yaxis_title="Design Quality Rating (Rating 1-5)"
                )
                st.plotly_chart(fig_scatter, use_container_width=True)

                # Aggregated Comparison (Bar Chart - Control Type)
                st.markdown("### Average Control Quality Score by Control Type")
                avg_score_by_type = filtered_df.groupby('Control_Type')['Control_Quality_Score'].mean().reset_index()
                fig_bar_type = px.bar(
                    avg_score_by_type,
                    x="Control_Type",
                    y="Control_Quality_Score",
                    color="Control_Type",
                    title="Average Control Quality Score by Control Type",
                    labels={
                        "Control_Type": "Control Type",
                        "Control_Quality_Score": "Average Quality Score"
                    },
                    color_discrete_sequence=px.colors.qualitative.Vivid
                )
                st.plotly_chart(fig_bar_type, use_container_width=True)

                # Aggregated Comparison (Bar Chart - Risk Level)
                st.markdown("### Average Control Quality Score by Risk Level")
                avg_score_by_risk = filtered_df.groupby('Risk_Level')['Control_Quality_Score'].mean().reset_index()
                # Ensure correct order for Risk Level
                risk_level_order = ["High", "Medium", "Low"]
                avg_score_by_risk['Risk_Level'] = pd.Categorical(avg_score_by_risk['Risk_Level'], categories=risk_level_order, ordered=True)
                avg_score_by_risk = avg_score_by_risk.sort_values('Risk_Level')

                fig_bar_risk = px.bar(
                    avg_score_by_risk,
                    x="Risk_Level",
                    y="Control_Quality_Score",
                    color="Risk_Level",
                    title="Average Control Quality Score by Risk Level",
                    labels={
                        "Risk_Level": "Risk Level",
                        "Control_Quality_Score": "Average Quality Score"
                    },
                    color_discrete_sequence=px.colors.qualitative.T10
                )
                st.plotly_chart(fig_bar_risk, use_container_width=True)


            else:
                st.warning("No data to display after filtering. Adjust your filters or generate/upload more data.")

        except (KeyError, TypeError, ValueError) as e:
            st.error(f"Data Processing Error: {e}")
            st.warning("Please ensure your CSV file has the required columns and correct data types, or adjust synthetic data generation parameters.")
    else:
        st.info("Please upload a CSV file or generate synthetic data to begin analysis.")
