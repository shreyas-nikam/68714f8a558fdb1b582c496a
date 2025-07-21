id: 68714f8a558fdb1b582c496a_documentation
summary: First lab of Module 3 Documentation
feedback link: https://docs.google.com/forms/d/e/1FAIpQLSfWkOK-in_bMMoHSZfcIvAeO58PAH9wrDqcxnJABHaxiDqhSA/viewform?usp=sf_link
environments: Web
status: Published
# Control Effectiveness Evaluator: A Streamlit Application Guide

## Introduction and Setup
Duration: 00:05:00

Welcome to the **Control Effectiveness Evaluator** Codelab! This guide will walk you through a Streamlit application designed to help you assess and analyze the quality of operational controls. Understanding control effectiveness is crucial in various domains like risk management, compliance, and internal audit, as it directly impacts an organization's ability to mitigate risks and achieve its objectives.

<aside class="positive">
<b>Operational Controls</b> are processes, policies, or activities designed to ensure that risks are contained within an organization's risk appetite. Evaluating their effectiveness helps identify weaknesses and improve overall risk posture.
</aside>

This application introduces two key concepts:
1.  **Control Quality Score**: A metric that quantifies the effectiveness of a control based on its attributes and observed implementation quality. A higher score generally indicates a more robust and reliable control.
2.  **Control Substantiation Method**: Suggested approaches for proving the effectiveness of a control (e.g., Re-performance, Examination, Inquiry) based on its characteristics and the associated risk level.

By the end of this codelab, you will:
*   Understand the architecture and modular design of a Streamlit application.
*   Learn how to evaluate individual controls based on defined criteria.
*   Explore how to load, validate, and analyze control data in bulk.
*   Gain insights into generating synthetic data for testing and analysis.
*   Understand the logic behind calculating the "Control Quality Score" and suggesting "Control Substantiation Methods."
*   Learn to create interactive visualizations with Plotly in Streamlit.

### Prerequisites

To follow along with this codelab, you'll need:
*   Python 3.8+ installed on your machine.
*   Basic understanding of Python programming.
*   Familiarity with Markdown syntax.

### Setting up your environment

1.  **Create a Project Directory**:
    ```bash
    mkdir control_evaluator_app
    cd control_evaluator_app
    ```

2.  **Create a Virtual Environment** (recommended):
    ```bash
    python -m venv venv
    ```
    *   On Windows:
        ```bash
        .\venv\Scripts\activate
        ```
    *   On macOS/Linux:
        ```bash
        source venv/bin/activate
        ```

3.  **Install Required Libraries**:
    ```bash
    pip install streamlit pandas plotly
    ```

4.  **Create Application Files**:
    You will create the following file structure:
    ```
    control_evaluator_app/
    ├── app.py
    └── application_pages/
        ├── __init__.py
        ├── home.py
        ├── evaluate_control.py
        └── analyze_data.py
    ```

    Create the `application_pages` directory and an empty `__init__.py` file inside it:
    ```bash
    mkdir application_pages
    touch application_pages/__init__.py
    ```

## Understanding the Application Structure
Duration: 00:10:00

The application follows a modular design, which helps in organizing the code for better readability, maintainability, and scalability. Streamlit applications often benefit from breaking down complex UIs into smaller, manageable components or pages.

### Core Application (`app.py`)

This is the main entry point of the Streamlit application. It sets up the page configuration, displays the header, and manages navigation between different sections of the app using Streamlit's sidebar.

Copy the following code into `app.py`:

```python
import streamlit as st
st.set_page_config(page_title="Control Effectiveness Evaluator", layout="wide")
st.sidebar.image("https://www.quantuniversity.com/assets/img/logo5.jpg")
st.sidebar.divider()
st.title("Control Effectiveness Evaluator")
st.divider()
st.markdown("""
Welcome to the Control Effectiveness Evaluator! This application helps you assess the design and implementation quality of operational controls. You can either upload your own control data in CSV format or generate synthetic data to explore different control scenarios. The application provides tools for defining control characteristics, calculating a 'Control Quality Score', and suggesting an appropriate 'Control Substantiation Method'.
""")
# Your code starts here
page = st.sidebar.selectbox(label="Navigation", options=["Home", "Evaluate Control", "Analyze Data"])
if page == "Home":
    from application_pages.home import run_home
    run_home()
elif page == "Evaluate Control":
    from application_pages.evaluate_control import run_evaluate_control
    run_evaluate_control()
elif page == "Analyze Data":
    from application_pages.analyze_data import run_analyze_data
    run_analyze_data()
# Your code ends
```

*   `st.set_page_config`: Configures the browser tab title and layout.
*   `st.sidebar`: Used for displaying the university logo, a divider, and the navigation selectbox.
*   `st.title` and `st.markdown`: Display the main title and an introductory text.
*   Navigation Logic: Based on the user's selection in the sidebar, the application dynamically imports and runs the corresponding function from the `application_pages` module. This is a common pattern for multi-page Streamlit apps.

### Application Pages (`application_pages/`)

This directory contains separate Python files for each major section of the application. This modular approach keeps the codebase organized.

*   `home.py`: The default landing page.
*   `evaluate_control.py`: For assessing individual control attributes.
*   `analyze_data.py`: For bulk data analysis and visualization.

<aside class="positive">
In a larger application, shared utility functions (like `calculate_control_quality_score` and `suggest_substantiation_method`) are typically placed in a separate `utils.py` file to avoid code duplication and improve maintainability. In the provided code, these functions are defined within `analyze_data.py` but imported by `evaluate_control.py`. For the purpose of this codelab, we will proceed, but it's a good practice to centralize such common logic.
</aside>

### Application Architecture Diagram

Below is a high-level representation of the application's structure and how different components interact:

```
+--+
|                                   |
|        Streamlit Application      |
|             (app.py)              |
|                                   |
++-+--+
          |
          |  Sidebar Navigation
          |  (st.sidebar.selectbox)
          |
+++
|                                                          |
|  +-+  +-+  +-+
|  |                |  |                   |  |                   |
|  |  Home Page     |  |  Evaluate Control |  |  Analyze Data     |
|  | (home.py)      |  | (evaluate_control.py) | (analyze_data.py) |
|  |                |  |                   |  |                   |
|  +-+  +++  +++
|                              |                         |
|                              | Calls                   | Handles
|                              |                         |
|                ++           |
|                | calculate_control_quality_score |       | Data Loading (CSV/Synthetic)
|                | suggest_substantiation_method   |       | Data Validation & Preprocessing
|                ++           | Data Analysis & Visualizations
|                                                         |
|                                                         |
|                        ++
|                        | External Data (CSV Upload) |
|                        ++
```

This diagram illustrates how `app.py` acts as the central orchestrator, directing user requests to specific modules within the `application_pages` directory. The `evaluate_control.py` page leverages shared logic (currently defined in `analyze_data.py`'s scope) to perform its calculations. The `analyze_data.py` page manages complex data workflows including ingestion, cleaning, and visualization.

## Exploring the Home Page
Duration: 00:02:00

The home page is the simplest part of the application, serving as an initial landing point and providing a brief introduction.

Create the file `application_pages/home.py` and add the following content:

```python
import streamlit as st

def run_home():
    st.header("Home")
    st.markdown("""
    This is the home page of the Control Effectiveness Evaluator. Use the navigation menu in the sidebar to explore the different sections of the application.
    """)
```

*   `st.header`: Displays a prominent header for the page.
*   `st.markdown`: Provides a short descriptive text.

**To run the application for the first time:**
Make sure your virtual environment is activated and you are in the `control_evaluator_app` directory.
```bash
streamlit run app.py
```
This command will open the application in your default web browser. You should see the "Home" page displayed, along with the sidebar navigation.

## Evaluating a Single Control
Duration: 00:15:00

This section allows users to define the characteristics of a single operational control and instantly receive a "Control Quality Score" and a "Suggested Substantiation Method." This is useful for quick assessments or understanding how different attributes influence the score and method.

Create the file `application_pages/evaluate_control.py` and add the following content:

```python
import streamlit as st

# These functions are defined in analyze_data.py in the provided code,
# but for the purpose of evaluate_control, we'll assume they are accessible.
# In a real application, these would typically be in a shared 'utils.py' file.
# For now, we'll just include their definitions here for clarity of this section.

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


def run_evaluate_control():
    st.header("Evaluate Control")
    st.markdown("""
    In this section, you can define the attributes of a single control and calculate its 'Control Quality Score' and suggested 'Control Substantiation Method'.
    """)

    control_types = ["Preventative", "Detective"]
    key_nonkey_options = ["Key", "Non-Key"]
    manual_automated_options = ["Manual", "Automated"]
    risk_level_options = ["High", "Medium", "Low"]

    control_type = st.selectbox("Control Type", options=control_types, help="Defines whether the control aims to prevent issues or detect them after they occur.")
    key_nonkey = st.selectbox("Key/Non-Key", options=key_nonkey_options, help="Indicates if the control is critical (Key) or supplementary (Non-Key).")
    manual_automated = st.selectbox("Manual/Automated", options=manual_automated_options, help="Specifies if the control execution is manual or automated.")
    risk_level = st.selectbox("Risk Level", options=risk_level_options, help="The inherent risk level the control aims to mitigate.")
    implementation_quality_rating = st.slider("Implementation Quality Rating", min_value=1, max_value=5, step=1, help="Observed quality of the control's execution (1 = Low, 5 = High).")

    if st.button("Calculate Score & Method"):
        try:
            # Assuming calculate_control_quality_score and suggest_substantiation_method are in scope
            control_quality_score = calculate_control_quality_score(control_type, key_nonkey, manual_automated, implementation_quality_rating)
            substantiation_method = suggest_substantiation_method(control_type, key_nonkey, manual_automated, risk_level)

            st.metric("Control Quality Score", value=control_quality_score)
            st.write(f"Suggested Substantiation Method: {substantiation_method}")
        except Exception as e:
            st.error(f"An error occurred: {e}")
```

Navigate to the "Evaluate Control" page in your running Streamlit application.

### Control Quality Score Calculation

The `calculate_control_quality_score` function assigns points based on control attributes and then adds the `implementation_quality_rating` (adjusted).

**Scoring Logic:**
*   **Control Type**:
    *   `Preventative`: +5 points (More effective as it stops issues before they occur)
    *   `Detective`: +2 points (Detects issues after they occur)
*   **Key/Non-Key**:
    *   `Key`: +3 points (Critical controls are more important)
    *   `Non-Key`: +1 point
*   **Manual/Automated**:
    *   `Automated`: +2 points (Generally more consistent and less prone to human error)
    *   `Manual`: +1 point
*   **Implementation Quality Rating (1-5)**: Added directly, but adjusted by subtracting 1. This means a rating of 1 adds 0 points, and a rating of 5 adds 4 points.
    *   `score += implementation_quality_rating - 1`

**Example:**
A "Preventative", "Key", "Automated" control with an "Implementation Quality Rating" of 5:
Score = 5 (Preventative) + 3 (Key) + 2 (Automated) + (5 - 1) (Implementation Quality) = 5 + 3 + 2 + 4 = **14**

### Suggested Substantiation Method

The `suggest_substantiation_method` function recommends an audit technique based on a combination of control attributes and the risk level it addresses.

**Rules:**
*   **Re-performance**: Often suggested for `Preventative`, `Key`, `Manual` controls, especially with `High` risk. This involves the auditor independently executing the control process.
*   **Examination**: Recommended for `Detective`, `Non-Key`, `Automated` controls with `Medium` risk, or `Preventative`, `Key`, `Manual` with `Medium` risk. This involves inspecting documents or records.
*   **Inquiry**: Suggested for `Preventative`, `Key`, `Manual` with `Low` risk, and as a default for other combinations. This involves asking questions of knowledgeable persons.
*   **Re-performance / Examination**: For `Detective`, `Non-Key`, `Automated` with `High` risk.

This logic reflects common auditing principles where higher risk or more critical controls require more rigorous substantiation.

Experiment with different combinations of inputs on this page to observe how the score and method change.

## Analyzing Control Data - Data Loading and Preprocessing
Duration: 00:20:00

The "Analyze Data" page is the most robust part of the application, allowing users to upload a dataset of controls or generate synthetic data for analysis. It includes critical steps like data loading, validation, preprocessing, and finally, analysis and visualization.

Create the file `application_pages/analyze_data.py` and add the following content:

```python
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
            st.error(f"Column '{col}' is missing. Please ensure your CSV has all required columns.")
            return None

    for col in ['Control_Type', 'Key_NonKey', 'Manual_Automated', 'Risk_Level', 'Control_ID']:
        # Check if all values are strings and not empty/whitespace
        if not df[col].apply(lambda x: isinstance(x, str) and x.strip() != '').all():
            st.error(f"Column '{col}' must contain non-empty string values.")
            return None

    for col in ['Implementation_Frequency', 'Design_Quality_Rating']:
        # Convert to numeric, coercing errors to NaN
        df[col] = pd.to_numeric(df[col], errors='coerce')
        # Check for NaNs introduced by coercion and ensure all values are numeric
        if df[col].isnull().any() or not all(pd.api.types.is_numeric_dtype(df[col])):
            st.error(f"Column '{col}' must contain numbers and cannot have missing or invalid values.")
            return None
        # Optionally, check for a valid range if necessary (e.g., 1-5 for ratings)
        if not (df[col].between(1, 5).all()): # Assuming these ratings are 1-5
            st.warning(f"Warning: Column '{col}' contains values outside the expected range of 1-5. Proceeding but review your data.")


    if df.isnull().any().any():
        critical_fields_for_null_check = [col for col in required_columns if col != 'Control_ID']
        # Check for nulls in critical columns after numeric conversion
        if df[critical_fields_for_null_check].isnull().any().any():
            st.error("DataFrame contains missing values in critical columns. Please fill or remove them.")
            return None

    if 'Control_ID' in df.columns and df['Control_ID'].duplicated().any():
        st.error("Control_ID contains duplicate values. Each control must have a unique ID.")
        return None

    return df

# Include the definition of these functions here as they are used later in this module
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
            df['Control_Quality_Score'] = df.apply(lambda row: calculate_control_quality_score(row['Control_Type'], row['Key_NonKey'], row['Manual_Automated'], row['Design_Quality_Rating']), axis=1)
            st.success("Control Quality Score calculated successfully for all records.")
        except Exception as e:
            st.error(f"Error calculating Control Quality Score: {e}. Please check your data's 'Design_Quality_Rating' and other relevant columns.")
            # If scoring fails, prevent further processing that relies on the score
            return

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
            st.error(f"Error creating visualizations: {e}. Ensure necessary numeric columns for plotting are present and valid.")
```

Navigate to the "Analyze Data" page in your running Streamlit application.

### Data Loading (`load_control_data`)

The application offers two ways to get data:
*   **Upload CSV**: Users can upload a CSV file containing their control data using `st.file_uploader`.
*   **Generate Synthetic Data**: For demonstration and testing, the application can create a dummy dataset. The `generate_synthetic_control_data` function populates a DataFrame with random values for control attributes. The number of records can be adjusted with a slider.

<aside class="negative">
When uploading your own CSV, ensure it contains the following columns for the application to function correctly:
`Control_Type`, `Key_NonKey`, `Manual_Automated`, `Risk_Level`, `Implementation_Frequency`, `Design_Quality_Rating`, `Control_ID`.
</aside>

### Data Validation and Preprocessing (`validate_and_preprocess_data`)

This is a crucial step for ensuring data quality and preventing errors in subsequent analysis. The `validate_and_preprocess_data` function performs several checks:
1.  **Required Columns**: Verifies that all expected columns are present.
2.  **String Type Check**: Ensures categorical columns (`Control_Type`, `Key_NonKey`, `Manual_Automated`, `Risk_Level`, `Control_ID`) contain string values.
3.  **Numeric Type Check**: Converts `Implementation_Frequency` and `Design_Quality_Rating` to numeric, and checks for `NaN` values introduced by conversion (indicating non-numeric data).
4.  **Missing Values**: Checks for any null values in critical columns.
5.  **Duplicate Control IDs**: Ensures each `Control_ID` is unique, which is essential for identifying individual controls.

<aside class="positive">
Robust data validation is essential for any data-driven application. It prevents unexpected crashes and provides clear feedback to the user about data quality issues.
</aside>

### Analyze Data Page Flowchart

This flowchart illustrates the steps involved when a user interacts with the "Analyze Data" page:

```
+--+
| Start Analyze Control Data     |
++-+
                |
                V
+--+
| User Interaction:              |
| - Upload CSV File              |
| - OR Generate Synthetic Data   |
++-+
                |
                V
+--+
| Load Control Data              |
| (load_control_data function)   |
|                                |
|   Is data loaded successfully? |
++-+
  No            | Yes
  |             V
  |   +--+
  |   | Validate & Preprocess Data   |
  |   | (validate_and_preprocess_data) |
  |   |                                |
  |   |   Is data valid and clean?     |
  V   ++-+
Display Error       No| Yes
Message               |
                      V
            +--+
            | Display Raw Data Table         |
            | (st.dataframe)                 |
            ++-+
                            |
                            V
            +--+
            | Display Summary Statistics     |
            | (df.describe(), value_counts)  |
            ++-+
                            |
                            V
            +--+
            | Calculate Control Quality Score|
            | (df.apply(calculate_control_quality_score)) |
            ++-+
                            |
                            V
            +--+
            | Generate & Display Visualizations|
            | (Plotly Express charts)        |
            ++-+
                            |
                            V
            +--+
            | End Analyze Control Data       |
            +--+
```

## Analyzing Control Data - Calculations and Visualizations
Duration: 00:20:00

Once the data is loaded and validated, the application proceeds to calculate the "Control Quality Score" for each record and then presents the data through summary statistics and interactive visualizations.

### Calculating Control Quality Score on DataFrame

The `Control_Quality_Score` logic, which we explored in the "Evaluate Control" section, is applied to every row of the loaded DataFrame. This is achieved using Pandas' `apply` method, which iterates through each row and passes its attributes to the `calculate_control_quality_score` function.

```python
df['Control_Quality_Score'] = df.apply(lambda row: calculate_control_quality_score(row['Control_Type'], row['Key_NonKey'], row['Manual_Automated'], row['Design_Quality_Rating']), axis=1)
```
The result is a new column named `Control_Quality_Score` added to the DataFrame, providing a quantifiable measure for each control.

<aside class="positive">
Using `df.apply` with `axis=1` is a common way to apply a custom function row-wise to a Pandas DataFrame. While powerful, for very large datasets, vectorized operations are generally more performant.
</aside>

### Summary Statistics

The application displays basic descriptive statistics for the numerical columns using `df.describe()`. Additionally, it shows value counts for categorical (object) columns, giving a quick overview of the distribution of different control attributes.

```python
st.subheader("Summary Statistics")
st.write(df.describe())
for col in df.select_dtypes(include='object'):
    st.write(f"Value counts for column '{col}':")
    st.write(df[col].value_counts())
```

These statistics help in understanding the dataset's characteristics at a glance.

### Visualizations with Plotly Express

The application uses `plotly.express` to generate interactive charts, providing visual insights into the control data.

1.  **Scatter Plot: Relationship between Implementation Frequency and Design Quality**
    ```python
    fig_scatter = px.scatter(df, x="Implementation_Frequency", y="Design_Quality_Rating", color="Control_Type", hover_data=["Control_ID", "Control_Quality_Score"],
                            title="Relationship between Implementation Frequency and Design Quality")
    fig_scatter.update_layout(xaxis_title="Implementation Frequency (1-5)", yaxis_title="Design Quality Rating (1-5)")
    st.plotly_chart(fig_scatter)
    ```
    *   **Purpose**: This chart visualizes how frequently a control is implemented versus its design quality rating.
    *   **Insights**: You can observe clusters or trends. For example, are highly-rated designs also frequently implemented? Are there "Detective" controls that are less frequently implemented but have high design quality? The `color="Control_Type"` allows for differentiation between preventative and detective controls, and `hover_data` provides additional details on hover.

2.  **Bar Chart: Average Control Quality Score by Control Type**
    ```python
    df_grouped = df.groupby("Control_Type")["Control_Quality_Score"].mean().reset_index()
    fig_bar = px.bar(df_grouped, x="Control_Type", y="Control_Quality_Score", title="Average Control Quality Score by Control Type")
    st.plotly_chart(fig_bar)
    ```
    *   **Purpose**: This chart directly compares the average quality score between "Preventative" and "Detective" control types.
    *   **Insights**: Based on the scoring logic, "Preventative" controls inherently receive a higher base score. This chart visually confirms that tendency and shows the average aggregated quality based on the dataset. It helps in quickly identifying which type of control generally exhibits higher quality within the evaluated population.

## Running and Interacting with the Application
Duration: 00:10:00

Now that all the code components are in place, let's run the full application and interact with its features.

### How to Run

1.  **Ensure all files are created**: Make sure `app.py`, `application_pages/__init__.py`, `application_pages/home.py`, `application_pages/evaluate_control.py`, and `application_pages/analyze_data.py` are correctly placed in your `control_evaluator_app` directory.
2.  **Activate your virtual environment**:
    *   On Windows: `.\venv\Scripts\activate`
    *   On macOS/Linux: `source venv/bin/activate`
3.  **Navigate to the root directory**: Make sure your terminal is in the `control_evaluator_app` directory where `app.py` is located.
4.  **Run the Streamlit command**:
    ```bash
    streamlit run app.py
    ```
    This command will automatically open a new tab in your web browser, displaying the Streamlit application.

### Interacting with the Application

1.  **Home Page**:
    *   This is the default view. It provides a brief introduction to the application.

2.  **Evaluate Control Page**:
    *   Select "Evaluate Control" from the sidebar navigation.
    *   Use the `st.selectbox` and `st.slider` widgets to define the characteristics of a hypothetical control:
        *   Control Type (Preventative/Detective)
        *   Key/Non-Key
        *   Manual/Automated
        *   Risk Level (High/Medium/Low)
        *   Implementation Quality Rating (1-5)
    *   Click the "Calculate Score & Method" button.
    *   Observe the calculated "Control Quality Score" and the "Suggested Substantiation Method" displayed below. Experiment with different combinations to see how the results change.

3.  **Analyze Data Page**:
    *   Select "Analyze Data" from the sidebar navigation.
    *   **Option 1: Generate Synthetic Data**:
        *   Check the "Generate synthetic data instead" checkbox.
        *   Adjust the "Number of records" slider to generate a desired number of dummy control entries.
        *   The application will automatically load, validate, process, and display the synthetic data along with summary statistics and visualizations.
    *   **Option 2: Upload Your Own CSV**:
        *   Uncheck the "Generate synthetic data instead" checkbox (if it's checked).
        *   Click the "Browse files" button under "Upload your control data (CSV format)".
        *   Select a CSV file from your computer that contains control data with the required columns (as mentioned in Step 5: `Control_Type`, `Key_NonKey`, `Manual_Automated`, `Risk_Level`, `Implementation_Frequency`, `Design_Quality_Rating`, `Control_ID`).
        *   If your data is valid, it will be displayed, analyzed, and visualized. If there are validation errors, the application will provide informative error messages.

<aside class="positive">
Experiment with generating different numbers of synthetic records to observe how the visualizations change and how the application handles larger datasets. You can also try uploading a malformed CSV (e.g., missing a column) to see the validation error messages.
</aside>

## Further Enhancements and Next Steps
Duration: 00:05:00

This Streamlit application provides a solid foundation for evaluating and analyzing operational controls. However, there are many avenues for further enhancement and expansion.

### Potential Enhancements

1.  **More Sophisticated Scoring Models**:
    *   Implement more complex algorithms for the Control Quality Score, perhaps incorporating weighted factors, expert systems, or even machine learning models trained on historical audit data.
    *   Allow users to customize the scoring weights for different control attributes.
    *   Introduce a 'Control Effectiveness Rating' or 'Maturity Level' system beyond a single score.

2.  **Advanced Substantiation Method Logic**:
    *   Expand the rules for suggesting substantiation methods to cover more nuanced scenarios and provide justifications for the recommendations.
    *   Integrate a knowledge base or decision tree for more dynamic method suggestions.

3.  **Database Integration**:
    *   Instead of relying on CSV uploads or synthetic data, integrate with a backend database (e.g., PostgreSQL, SQLite) to store and manage control data persistently.
    *   Allow users to save their control evaluations and view historical trends.

4.  **User Authentication and Authorization**:
    *   For enterprise use, add user login and role-based access control to protect sensitive control data.

5.  **Additional Visualizations and Reporting**:
    *   Implement more chart types (e.g., pie charts for categorical distributions, heatmaps for correlations).
    *   Generate downloadable PDF/Excel reports summarizing the analysis.
    *   Allow filtering and slicing of data within the "Analyze Data" section for more granular insights.

6.  **Benchmarking and Comparison**:
    *   Enable users to compare their control scores against industry benchmarks or historical averages.

7.  **Alerting and Anomaly Detection**:
    *   Set up alerts for controls falling below a certain quality score or exhibiting unusual patterns.

8.  **Interactive Data Input for Analysis Page**:
    *   Instead of only uploading or generating, allow users to manually add or edit records directly within the "Analyze Data" page via Streamlit widgets.

### Next Steps for Developers

*   **Refactor Shared Logic**: Move `calculate_control_quality_score` and `suggest_substantiation_method` into a separate `utils.py` file within the `application_pages` directory (or a new `src` directory) and import them into both `evaluate_control.py` and `analyze_data.py`. This improves code organization.

    Example `application_pages/utils.py`:
    ```python
    # common utility functions here
    def calculate_control_quality_score(...):
        # ...
    def suggest_substantiation_method(...):
        # ...
    ```
    Then, in `evaluate_control.py` and `analyze_data.py`:
    ```python
    from application_pages.utils import calculate_control_quality_score, suggest_substantiation_method
    ```

*   **Error Handling**: Enhance error handling to be more specific and user-friendly, guiding users on how to fix data issues.
*   **Unit Testing**: Write unit tests for the core logic functions (e.g., `calculate_control_quality_score`, `suggest_substantiation_method`, `validate_and_preprocess_data`) to ensure their correctness.
*   **Deployment**: Learn how to deploy your Streamlit application to cloud platforms like Streamlit Community Cloud, Heroku, or AWS.

We hope this codelab has provided you with a comprehensive understanding of the Control Effectiveness Evaluator application and inspired you to explore its functionalities and potential extensions!

