
# Streamlit Application Requirements Specification

## 1. Application Overview

The **Control Effectiveness Evaluator** Streamlit application aims to guide users through assessing the design and implementation quality of operational controls. Designed for internal auditors, risk analysts, and process owners, it provides a hands-on experience with control attributes and evaluation methodologies. The application will leverage a synthetic dataset to simulate various control scenarios and their assessment outcomes, ensuring quick execution on mid-spec laptops.

**Objectives:**
*   To enable users to understand the key attributes of operational controls (e.g., preventative vs. detective, key vs. non-key, manual vs. automated) as discussed in the `PRMIA Operational Risk Manager Handbook` [1].
*   To allow users to apply theoretical knowledge by defining control characteristics and immediately seeing implications for assessment methodology and perceived quality.
*   To provide different methods for evaluating control effectiveness, such as re-performance, observation, examination, and inquiry [2].
*   To calculate and display a qualitative 'Control Quality Score' and suggest an appropriate 'Control Substantiation Method' based on user-defined control attributes and implementation quality.
*   To visualize correlations between control attributes and derived quality scores, and to compare distributions of different control types and their average scores.

**Constraints:**
*   The application must execute end-to-end in fewer than 5 minutes.
*   Only open-source Python libraries from PyPI may be used.

## 2. User Interface Requirements

### 2.1. Layout and Navigation Structure

The application will feature a clear, intuitive layout structured into logical sections:
*   **Header:** Displaying the application title "Control Effectiveness Evaluator."
*   **Overview Section:** A brief introduction to the application's purpose and learning outcomes.
*   **Data Input Section:** Allows users to load data or generate synthetic data.
*   **Interactive Control Definition Section:** For defining attributes of a single control for individual assessment.
*   **Results Display Section:** Shows the calculated 'Control Quality Score' and 'Suggested Substantiation Method'.
*   **Data Analysis & Visualization Section:** Presents insights from the loaded/generated dataset through interactive charts and tables.
*   **References Section:** Credits external datasets or libraries used, including the `PRMIA Operational Risk Manager Handbook` [1, 2].

### 2.2. Input Widgets and Controls

**a. Data Loading Options:**
*   **File Uploader:** An `st.file_uploader` widget to allow users to upload their own CSV file containing control data.
    *   Description: "Upload your control data (CSV format)"
*   **Synthetic Data Generation Checkbox:** An `st.checkbox` to opt for generating synthetic data if no file is uploaded.
    *   Description: "Generate synthetic data instead"
*   **Number of Records (for synthetic data):** An `st.slider` or `st.number_input` to specify `num_records` for synthetic data generation (e.g., range 5 to 1000).
    *   Tooltip/Help Text: "Number of synthetic control records to generate. Adjust for performance."

**b. Individual Control Definition (for single control evaluation):**
*   **Control Type:** `st.selectbox` with options: ["Preventative", "Detective"].
    *   Tooltip: "Defines whether the control aims to prevent issues or detect them after they occur."
*   **Key/Non-Key:** `st.selectbox` with options: ["Key", "Non-Key"].
    *   Tooltip: "Indicates if the control is critical (Key) or supplementary (Non-Key)."
*   **Manual/Automated:** `st.selectbox` with options: ["Manual", "Automated"].
    *   Tooltip: "Specifies if the control execution is manual or automated."
*   **Risk Level:** `st.selectbox` with options: ["High", "Medium", "Low"].
    *   Tooltip: "The inherent risk level the control aims to mitigate."
*   **Implementation Quality Rating:** `st.slider` with range 1 to 5 (integer steps).
    *   Tooltip: "Observed quality of the control's execution (1 = Low, 5 = High)."
*   **"Calculate Score & Method" Button:** `st.button` to trigger the calculation.

### 2.3. Visualization Components

*   **Data Table Display:** `st.dataframe` to display the loaded or generated raw data.
*   **Summary Statistics:** `st.write` or `st.dataframe` to show `df.describe()` for numeric columns and value counts for categorical columns.
*   **Relationship Plot (Scatter Plot):** An interactive scatter plot (e.g., using Plotly Express) to visualize correlations.
    *   X-axis: `Implementation_Frequency`
    *   Y-axis: `Design_Quality_Rating`
    *   Color: `Control_Type` or `Control Quality Score` (if calculated for dataset).
    *   Title: "Relationship between Implementation Frequency and Design Quality"
    *   Labelled Axes: Clear labels (e.g., "Implementation Frequency (1-5)", "Design Quality Rating (1-5)").
    *   Interactivity: Zoom, pan, tooltips on hover.
*   **Aggregated Comparison (Bar Chart or Heatmap):**
    *   **Bar Chart:** Average 'Control Quality Score' by `Control_Type` or `Key_NonKey`.
        *   Title: "Average Control Quality Score by Control Type" (or other category)
        *   Labelled Axes and Legends.
    *   **Heatmap:** Average 'Control Quality Score' across two categorical attributes (e.g., `Control_Type` vs. `Key_NonKey`).
        *   Title: "Average Control Quality Score by Control Type and Key/Non-Key Status"
        *   Labelled Axes and Legends.
*   **Styling:**
    *   Color-blind-friendly palette will be adopted for all visualizations.
    *   Font size $\geq 12$ pt for titles, labels, and legends.
    *   Static fallback (saved PNG) will be provided for plots if interactive libraries are unavailable or explicitly requested.

### 2.4. Interactive Elements and Feedback Mechanisms

*   Real-time updates of results and visualizations upon input changes.
*   Display of calculated 'Control Quality Score' as a prominent metric.
*   Display of suggested 'Control Substantiation Method' with a clear explanation.
*   Informative error messages (e.g., `st.error`) for validation failures (`FileNotFoundError`, `KeyError`, `TypeError`, `ValueError`).
*   Success messages (e.g., `st.success`) for successful data loading and validation.

## 3. Additional Requirements

*   **Real-time Updates and Responsiveness:** The Streamlit application will inherently provide real-time updates as users interact with the input widgets, ensuring immediate feedback on control assessments and data visualizations.
*   **Annotation and Tooltip Specifications:** All interactive input widgets will include inline help text or tooltips (using `help` parameter in Streamlit widgets) to clearly describe the purpose and expected input for each control, enhancing user understanding and usability.
*   **Performance:** The application will be optimized for quick execution, particularly with the synthetic data generation, to meet the sub-5-minute execution requirement on mid-spec laptops.

## 4. Notebook Content and Code Requirements

This section details the functions extracted from the Jupyter Notebook and their integration into the Streamlit application.

### 4.1. `generate_synthetic_control_data` Function

**Description:** This function creates a Pandas DataFrame populated with randomized synthetic control data based on specified attributes. It serves as a lightweight sample dataset when no user data is provided.

**Code:**
```python
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
        "Control_ID": [f"C{i+1}" for i in range(num_records)] # Added Control_ID for validation
    }
    return pd.DataFrame(data)
```

**Integration into Streamlit:**
*   This function will be called if the user opts for "Generate synthetic data" and no file is uploaded.
*   `num_records` will be linked to an `st.slider` or `st.number_input`.
*   The categorical lists (`control_type`, `key_nonkey`, etc.) will be pre-defined lists within the Streamlit application (e.g., `["Preventative", "Detective"]`) to ensure consistency and use as options for `random.choice`.

### 4.2. `load_control_data` Function

**Description:** This function loads control data from a specified CSV file path. If no file path is provided, it can generate a simple synthetic DataFrame (though the main synthetic data generation will use the more comprehensive `generate_synthetic_control_data`). This function is critical for handling user uploads or default data loading.

**Code:**
```python
import pandas as pd

def load_control_data(file_path, generate_synthetic):
    """Loads control data from a file or generates synthetic data (simple placeholder)."""
    if file_path:
        try:
            df = pd.read_csv(file_path)
            return df
        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {file_path}")
        except pd.errors.EmptyDataError:
            return pd.DataFrame() # Return empty DataFrame for empty file
        except Exception as e:
            raise Exception(f"Error loading file: {e}")
    elif generate_synthetic:
        # This branch will be replaced by a call to generate_synthetic_control_data with full parameters
        # For now, keeping original notebook behavior for a "simple" synthetic df if generate_synthetic is True
        return pd.DataFrame({'col1': [1, 2, 3], 'col2': [4, 5, 6]}) # This will be replaced
    else:
        raise ValueError("Either file_path must be provided or generate_synthetic must be True.")
```

**Integration into Streamlit:**
*   `file_path` will be sourced from `st.file_uploader` (a `UploadedFile` object).
*   The `generate_synthetic` flag will come from an `st.checkbox`.
*   The Streamlit app will prioritize user upload. If no file is uploaded, it will check the `generate_synthetic` checkbox. If true, it will then call the more comprehensive `generate_synthetic_control_data` function instead of the placeholder `pd.DataFrame({'col1': [1, 2, 3], 'col2': [4, 5, 6]})`.
*   Error handling (e.g., `try-except FileNotFoundError`) will be implemented using `st.error` messages.

### 4.3. `validate_and_preprocess_data` Function

**Description:** This function ensures the integrity and consistency of the control data by checking for required columns, correct data types, and the absence of missing or duplicate `Control_ID` values.

**Code:**
```python
import pandas as pd

def validate_and_preprocess_data(df):
    """Validates and preprocesses the control data."""

    required_columns = ['Control_Type', 'Key_NonKey', 'Manual_Automated', 'Risk_Level',
                        'Implementation_Frequency', 'Design_Quality_Rating', 'Control_ID']
    for col in required_columns:
        if col not in df.columns:
            raise KeyError(f"Column '{col}' is missing.")

    for col in ['Control_Type', 'Key_NonKey', 'Manual_Automated', 'Risk_Level', 'Control_ID']:
        # Ensure that non-string values are caught if they exist after initial load
        if not df[col].apply(lambda x: isinstance(x, str)).all():
            raise TypeError(f"Column '{col}' must contain strings.")

    for col in ['Implementation_Frequency', 'Design_Quality_Rating']:
        # Convert to numeric first to handle potential strings that are numbers
        df[col] = pd.to_numeric(df[col], errors='coerce')
        if df[col].isnull().any() or not all(pd.api.types.is_numeric_dtype(df[col])):
             raise TypeError(f"Column '{col}' must contain numbers.")

    if df.isnull().any().any():
        # Exclude Control_ID from null check if it's auto-generated for synthetic data
        # For uploaded data, all critical fields must be non-null.
        critical_fields_for_null_check = [col for col in required_columns if col != 'Control_ID']
        if df[critical_fields_for_null_check].isnull().any().any():
            raise ValueError("DataFrame contains missing values in critical columns.")

    if 'Control_ID' in df.columns and df['Control_ID'].duplicated().any():
        raise ValueError("Control_ID contains duplicate values.")

    return df
```

**Integration into Streamlit:**
*   This function will be called immediately after `load_control_data` (or `generate_synthetic_control_data`) to ensure data quality before any analysis or visualization.
*   Error messages (e.g., `st.error`) will be displayed for each specific validation failure (missing columns, wrong types, missing values, duplicates).
*   A `try-except` block around this call will catch validation exceptions.

### 4.4. `calculate_control_quality_score` Function

**Description:** This function quantifies the perceived strength and effectiveness of an operational control based on its attributes and observed implementation quality, following the handbook's guidance [1].

**Formula:**
The 'Control Quality Score' is a conceptual representation, derived from weighted factors based on the handbook's guidance:
$$\text{Control Quality Score} = \sum_{i=1}^{N}(\text{weight}_{\text{attribute}_i} \cdot \text{score}_{\text{attribute}_i}) + \text{Implementation Quality Rating}$$
Where:
*   $\text{weight}_{\text{attribute}_i}$ represents the predefined weight for a specific control attribute (e.g., Preventative, Key, Automated).
*   $\text{score}_{\text{attribute}_i}$ represents the score assigned to that attribute's value.
*   $\text{Implementation Quality Rating}$ is a direct input reflecting the observed quality of the control's execution. The input rating is adjusted by subtracting 1 to align with a scoring scale where a rating of 1 contributes 0 to the score, a rating of 5 contributes 4, etc.

**Scoring Logic:**
*   **Control Type:** 'Preventative' (5 points), 'Detective' (2 points).
*   **Key/Non-Key:** 'Key' (3 points), 'Non-Key' (1 point).
*   **Manual/Automated:** 'Automated' (2 points), 'Manual' (1 point).
*   **Implementation Quality Rating:** Directly added to the sum, adjusted by subtracting 1 (e.g., a rating of 5 adds 4 to the score).

**Code:**
```python
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
```

**Integration into Streamlit:**
*   **Individual Assessment:** This function will be called using values from `st.selectbox` and `st.slider` widgets in the "Interactive Control Definition" section. The result will be displayed using `st.metric` or `st.write`.
*   **Dataset Analysis:** This function will be applied row-wise to the validated DataFrame (using `df.apply` or a loop) to calculate a 'Control_Quality_Score' column for each control in the dataset. This new column will then be used for visualizations.

### 4.5. `suggest_substantiation_method` Function

**Description:** This function recommends the most appropriate control substantiation method based on the control's attributes and its associated risk level, derived from the `PRMIA Operational Risk Manager Handbook` [2].

**Lookup Logic:**
The suggested method is determined by conditional rules considering:
*   `Control_Type`: Preventative or Detective
*   `Key_NonKey`: Key or Non-Key
*   `Manual_Automated`: Manual or Automated
*   `Risk_Level`: High, Medium, or Low

**Code:**
```python
def suggest_substantiation_method(control_type, key_nonkey, manual_automated, risk_level):
    """Suggests substantiation method based on control attributes and risk level."""

    # Input validation for robustness
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
```

**Integration into Streamlit:**
*   **Individual Assessment:** This function will be called using values from `st.selectbox` widgets in the "Interactive Control Definition" section. The recommended method will be displayed using `st.write`.
*   **Dataset Analysis:** This function will be applied row-wise to the validated DataFrame to calculate a 'Suggested_Method' column for each control in the dataset. This column can be displayed in the data table.
*   Error handling for invalid inputs will be implemented using `st.error` messages.

### 4.6. Data for Synthetic Generation & Default Options

The following lists will be used to populate selectbox/multiselect options and for generating synthetic data:

```python
control_types = ["Preventative", "Detective"]
key_nonkey_options = ["Key", "Non-Key"]
manual_automated_options = ["Manual", "Automated"]
risk_level_options = ["High", "Medium", "Low"]
implementation_frequency_range = [1, 2, 3, 4, 5] # For sliders/random choice
design_quality_rating_range = [1, 2, 3, 4, 5] # For sliders/random choice
```

### 4.7. Visualizations Implementation

*   The Streamlit application will import `plotly.express` for interactive plots.
*   A `st.session_state` variable will be used to store the loaded/generated DataFrame to avoid re-running data loading/generation on every interaction.
*   For the relationship plot, `px.scatter(df, x="Implementation_Frequency", y="Design_Quality_Rating", color="Control_Type", hover_data=["Control_ID", "Control_Quality_Score"])` will be used.
*   For aggregated comparison, `df.groupby("Control_Type")["Control_Quality_Score"].mean().reset_index()` followed by `px.bar` will be used for a bar chart. For a heatmap, `df.groupby(["Control_Type", "Key_NonKey"])["Control_Quality_Score"].mean().unstack()` will be prepared, then passed to `px.imshow`.
*   Plots will be displayed using `st.plotly_chart`.

