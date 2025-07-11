
# Streamlit Application Requirements Specification: Control Effectiveness Evaluator

This document outlines the requirements for developing a Streamlit application based on the provided Jupyter Notebook content and user specifications. It details the application's purpose, user interface components, interactive elements, and how the existing Python code will be integrated.

## 1. Application Overview

The **Control Effectiveness Evaluator** is an interactive Streamlit application designed to facilitate the understanding and assessment of operational control attributes and evaluation methodologies. It serves as a practical tool for internal auditors, risk analysts, and process owners.

**Purpose and Objectives:**
*   To provide a hands-on experience in defining and evaluating operational controls.
*   To enable users to apply theoretical knowledge from the `PRMIA Operational Risk Manager Handbook` regarding control attributes and assessment methods.
*   To calculate a qualitative 'Control Quality Score' based on user inputs and provide a suggested control substantiation method.
*   To visualize relationships between control attributes and derived scores using a synthetic or uploaded dataset.
*   To ensure quick execution (under 5 minutes on a mid-spec laptop) using open-source Python libraries.

## 2. User Interface Requirements

The application will feature a clear layout with interactive components to guide the user through control assessment.

### 2.1 Layout and Navigation Structure

The application will use a sidebar for primary user inputs and navigation, with the main area dedicated to displaying results, data tables, and visualizations.

*   **Sidebar:** Will host input widgets for data source selection (upload or synthetic generation) and potentially filters for dataset analysis mode. It will also contain input forms for "Define a Single Control" mode.
*   **Main Content Area:** Will dynamically display content based on the selected mode:
    *   Application title and overview.
    *   Input forms and results for single control evaluation.
    *   Data display (table) for loaded/generated datasets.
    *   Interactive visualizations (scatter plots, bar charts).
    *   Formulas and references.
*   **Navigation Modes:** A clear switch (e.g., `st.radio` or `st.tabs`) will allow users to choose between:
    *   **"Define a Single Control":** For evaluating individual control scenarios.
    *   **"Analyze Control Dataset":** For loading/generating and visualizing aggregate control data.

### 2.2 Input Widgets and Controls

Interactive widgets will allow users to configure control scenarios and load data.

*   **Data Source Selection (in Sidebar, affecting "Analyze Control Dataset" mode):**
    *   **Data Source Option (`st.radio`):** "Upload CSV File" or "Generate Synthetic Data".
    *   **CSV Upload (`st.file_uploader`):** Appears if "Upload CSV File" is selected. Accepts `.csv` files.
        *   _Help Text:_ "Upload a CSV file containing control data with columns: Control_Type, Key_NonKey, Manual_Automated, Risk_Level, Implementation_Frequency, Design_Quality_Rating, Control_ID."
    *   **Synthetic Data Generation (`st.number_input`):** Appears if "Generate Synthetic Data" is selected.
        *   _Input:_ `num_records` (integer, default 50, min 10, max 1000).
        *   _Help Text:_ "Specify the number of synthetic control records to generate for analysis. A larger number may take slightly longer to process."

*   **Single Control Input Form (in Main Area, for "Define a Single Control" mode):**
    *   **Control Type (`st.selectbox`):** Options: "Preventative", "Detective".
        *   _Help Text:_ "Select whether the control aims to prevent an issue before it occurs (Preventative) or detect it after (Detective)."
    *   **Key/Non-Key (`st.selectbox`):** Options: "Key", "Non-Key".
        *   _Help Text:_ "Indicate if this is a primary control (Key) or a supporting one (Non-Key)."
    *   **Manual/Automated (`st.selectbox`):** Options: "Manual", "Automated".
        *   _Help Text:_ "Choose if the control is performed manually or by an automated system."
    *   **Risk Level (`st.selectbox`):** Options: "High", "Medium", "Low".
        *   _Help Text:_ "Specify the inherent risk level associated with this control."
    *   **Implementation Quality Rating (`st.slider`):** Range 1 to 5 (integer, default 3).
        *   _Help Text:_ "Rate the observed quality of the control's implementation (1: Poor, 5: Excellent)."
    *   **Calculate Button (`st.button`):** "Calculate Control Quality and Suggest Method".

*   **Dataset Filtering Controls (in Sidebar, for "Analyze Control Dataset" mode, after data is loaded/generated):**
    *   **Control Type Filter (`st.multiselect`):** Options from loaded data's `Control_Type` column.
    *   **Key/Non-Key Filter (`st.multiselect`):** Options from loaded data's `Key_NonKey` column.
    *   **Manual/Automated Filter (`st.multiselect`):** Options from loaded data's `Manual_Automated` column.
    *   **Risk Level Filter (`st.multiselect`):** Options from loaded data's `Risk_Level` column.
    *   **Numerical Range Sliders (`st.slider`):** For `Implementation_Frequency` and `Design_Quality_Rating` (e.g., `min_value` to `max_value` of the column).

### 2.3 Visualization Components

The application will display tabular data and interactive charts to provide insights.

*   **Data Table (`st.dataframe`):** Displays the raw or filtered control data, including calculated `Control_Quality_Score` and `Suggested_Method` columns.
*   **Core Visuals (using Altair for interactivity):**
    *   **Relationship Plot (Scatter Plot):**
        *   _Purpose:_ To examine correlations between numerical control attributes (`Implementation_Frequency`, `Design_Quality_Rating`) and the `Control_Quality_Score`.
        *   _Axes:_ `Implementation_Frequency` (X-axis), `Design_Quality_Rating` (Y-axis).
        *   _Encoding:_ Point size or color by `Control_Quality_Score`, color by `Control_Type` or `Risk_Level`.
        *   _Interactivity:_ Zoom and pan.
        *   _Title:_ "Relationship between Control Attributes and Quality Score".
    *   **Aggregated Comparison (Bar Chart):**
        *   _Purpose:_ To show the distribution and average `Control_Quality_Score` across different categorical control types.
        *   _Axes:_ Categorical attribute (e.g., `Control_Type`, `Risk_Level`, `Key_NonKey`, `Manual_Automated`) on X-axis, Average `Control_Quality_Score` on Y-axis.
        *   _Title Example:_ "Average Control Quality Score by Control Type".
    *   **Style & Usability:** All visuals will adopt a color-blind-friendly palette, have clear titles, labeled axes, and legends. Font size will be legible (Streamlit's default often meets >= 12 pt).
    *   **Static Fallback:** While Altair charts are interactive, if an environment does not support interactivity, Streamlit's native export functions or `st.pyplot` with Matplotlib (saved as PNG) could serve as a static fallback. For this specification, interactive Altair charts are the primary implementation.

### 2.4 Interactive Elements and Feedback Mechanisms

*   **Dynamic Updates:** All outputs (scores, methods, tables, charts) will update in real-time as user inputs or filters are changed.
*   **Validation Feedback:**
    *   `st.success`: For successful data loading, validation, or calculation.
    *   `st.error`: For data validation errors (e.g., missing columns, incorrect types, missing values, duplicate IDs) or calculation errors.
    *   `st.warning`: For advisory messages (e.g., "Please upload a file or generate synthetic data").
*   **Tooltips/Help Text:** All input widgets will include `help` attributes to provide inline explanations, as detailed in Section 2.2.

## 3. Additional Requirements

### 3.1 Real-time Updates and Responsiveness

The Streamlit framework inherently provides real-time updates as users interact with widgets. This ensures a highly responsive application experience where results are immediately reflected upon input changes, fulfilling the requirement for a fast execution time on mid-spec laptops.

### 3.2 Annotation and Tooltip Specifications

*   **Input Widgets:** Every interactive input widget (e.g., `st.selectbox`, `st.slider`, `st.file_uploader`, `st.number_input`) will utilize the `help` parameter to provide concise, informative tooltips or inline explanations to guide the user.
*   **Visualizations:** Interactive charts (e.g., Altair charts) will be configured to display detailed information on hover (tooltips) for data points. Chart titles, axis labels, and legends will be clear and descriptive.

## 4. Notebook Content and Code Requirements

This section details how the core Python functions and logic from the Jupyter Notebook will be implemented within the Streamlit application. Performance will be optimized using Streamlit's caching mechanisms.

### 4.1 Data Generation: `generate_synthetic_control_data`

This function will be used when the user selects to generate synthetic data, ensuring that the generated dataset includes realistic categorical and numerical fields.

*   **Original Function Signature:**
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
        }
        return pd.DataFrame(data)
    ```
*   **Integration Details:**
    *   This function will be called internally when the user opts for "Generate Synthetic Data" in the Streamlit UI.
    *   The `num_records` will come from an `st.number_input` widget.
    *   The lists for `control_type`, `key_nonkey`, `manual_automated`, `risk_level`, `implementation_frequency`, and `design_quality_rating` will be predefined based on the example usage in the Jupyter Notebook:
        ```python
        control_type_options = ["Preventative", "Detective"]
        key_nonkey_options = ["Key", "Non-Key"]
        manual_automated_options = ["Manual", "Automated"]
        risk_level_options = ["High", "Medium", "Low"]
        implementation_frequency_options = [1, 2, 3, 4, 5]
        design_quality_rating_options = [1, 2, 3, 4, 5]
        ```
    *   **Crucial Modification:** Since `validate_and_preprocess_data` requires a `Control_ID` column, a unique `Control_ID` will be added to the DataFrame immediately after it is generated:
        ```python
        synthetic_data['Control_ID'] = [f'C{i+1:04d}' for i in range(len(synthetic_data))]
        ```

### 4.2 Data Loading: `load_control_data` (Streamlit Adapted)

The data loading function will be adapted for Streamlit's file uploader and integrate the synthetic data generation.

*   **Original Function Signature:**
    ```python
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
            df = pd.DataFrame({'col1': [1, 2, 3], 'col2': [4, 5, 6]}) # Dummy data in notebook
            return df
        else:
            raise ValueError("Either file_path must be provided or generate_synthetic must be True.")
    ```
*   **Integration Details (Adapted for Streamlit):**
    *   A Streamlit-specific wrapper function will be created and decorated with `@st.cache_data` for performance.
    *   It will handle either a `st.file_uploader` output or trigger `generate_synthetic_control_data`.
    ```python
    import streamlit as st
    import pandas as pd
    # Assuming generate_synthetic_control_data is defined as above

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
            # Add Control_ID for synthetic data
            df['Control_ID'] = [f'C{i+1:04d}' for i in range(len(df))]
        else:
            st.info("Please select a data source to begin analysis.")
        return df
    ```

### 4.3 Data Validation and Preprocessing: `validate_and_preprocess_data`

This function is critical for data integrity and will be executed immediately after data loading/generation. Any errors will be communicated to the user.

*   **Original Function Signature:**
    ```python
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
            # Added robust numeric conversion for input data
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
    ```
*   **Integration Details:**
    *   After `load_control_data_streamlit` returns a DataFrame, it will be passed to this function within a `try-except` block to catch validation errors.
    *   Error messages (`KeyError`, `TypeError`, `ValueError`) will be displayed using `st.error`.
    *   If validation is successful, `st.success` will confirm.
    ```python
    # In Streamlit app flow:
    if not raw_df.empty:
        try:
            processed_df = validate_and_preprocess_data(raw_df.copy()) # Pass a copy
            st.success("Data loaded and validated successfully!")
            st.subheader("Validated Data Sample:")
            st.dataframe(processed_df.head())
        except (KeyError, TypeError, ValueError) as e:
            st.error(f"Data Validation Error: {e}")
            processed_df = pd.DataFrame() # Ensure DataFrame is empty if validation fails
    ```

### 4.4 Control Quality Score Calculation: `calculate_control_quality_score`

This function will calculate the score for single control evaluations and as a new column for dataset analysis.

*   **Original Function Signature:**
    ```python
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
    ```
*   **Formula Display (using `st.latex`):**
    $$ \text{Control Quality Score} = \sum_{i=1}^{N}(\text{weight}_{\text{attribute}_i} \cdot \text{score}_{\text{attribute}_i}) + \text{Implementation Quality Rating} $$
*   **Integration Details:**
    *   **Single Control Mode:** Input values from the `st.selectbox` and `st.slider` widgets will be passed to this function. The resulting score will be displayed using `st.metric` or `st.write`.
    *   **Dataset Mode:** This function will be applied row-wise to the validated DataFrame to create a new `Control_Quality_Score` column. It is assumed that the `Implementation_Frequency` column in the dataset serves as the `implementation_quality_rating` for this calculation, as per the notebook's conceptual model.
        ```python
        # In Streamlit app flow (for Dataset Mode, after validation):
        if not processed_df.empty:
            try:
                processed_df['Control_Quality_Score'] = processed_df.apply(
                    lambda row: calculate_control_quality_score(
                        row['Control_Type'],
                        row['Key_NonKey'],
                        row['Manual_Automated'],
                        row['Implementation_Frequency'] # Using Implementation_Frequency as the rating input
                    ), axis=1
                )
            except Exception as e:
                st.error(f"Error calculating Control Quality Score: {e}")
                processed_df = pd.DataFrame() # Clear dataframe on calculation error
        ```

### 4.5 Control Substantiation Method Suggestion: `suggest_substantiation_method`

This function will recommend the most appropriate substantiation method.

*   **Original Function Signature:**
    ```python
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
    ```
*   **Integration Details:**
    *   **Single Control Mode:** Input values from the `st.selectbox` widgets will be passed. The suggested method will be displayed using `st.info` or `st.write`.
    *   **Dataset Mode:** This function will be applied row-wise to the DataFrame to create a new `Suggested_Method` column.
        ```python
        # In Streamlit app flow (for Dataset Mode, after score calculation):
        if not processed_df.empty:
            processed_df['Suggested_Method'] = processed_df.apply(
                lambda row: suggest_substantiation_method(
                    row['Control_Type'],
                    row['Key_NonKey'],
                    row['Manual_Automated'],
                    row['Risk_Level']
                ), axis=1
            )
        ```

### 4.6 Visualization Implementation

Streamlit's `st.altair_chart` will be used for interactive plots.

*   **Scatter Plot (`Control_Quality_Score` vs. `Implementation_Frequency` vs. `Design_Quality_Rating`):**
    ```python
    import altair as alt
    # Assuming processed_df is available and has 'Control_Quality_Score', 'Implementation_Frequency', 'Design_Quality_Rating', etc.
    if not processed_df.empty and 'Control_Quality_Score' in processed_df.columns:
        scatter_chart = alt.Chart(processed_df).mark_circle(size=60).encode(
            x=alt.X('Implementation_Frequency:Q', title='Implementation Frequency (Rating 1-5)', scale=alt.Scale(domain=[0.5, 5.5])),
            y=alt.Y('Design_Quality_Rating:Q', title='Design Quality Rating (Rating 1-5)', scale=alt.Scale(domain=[0.5, 5.5])),
            color=alt.Color('Control_Type:N', title='Control Type', scale=alt.Scale(range='viridis')), # Color-blind friendly palette
            size=alt.Size('Control_Quality_Score:Q', title='Quality Score', legend=alt.Legend(titleFontSize=12, labelFontSize=12)),
            tooltip=[
                'Control_ID',
                'Control_Type',
                'Key_NonKey',
                'Manual_Automated',
                'Risk_Level',
                'Implementation_Frequency',
                'Design_Quality_Rating',
                'Control_Quality_Score',
                'Suggested_Method'
            ]
        ).properties(
            title={
                "text": "Control Quality vs. Implementation & Design",
                "fontSize": 16,
                "anchor": "middle"
            }
        ).interactive()
        st.subheader("Relationship Plot: Control Quality Score")
        st.altair_chart(scatter_chart, use_container_width=True)
    ```

*   **Bar Charts (Aggregated Comparisons):**
    ```python
    # Example: Average score by Control Type
    if not processed_df.empty and 'Control_Quality_Score' in processed_df.columns:
        avg_score_by_type = processed_df.groupby('Control_Type')['Control_Quality_Score'].mean().reset_index()
        bar_chart_type = alt.Chart(avg_score_by_type).mark_bar().encode(
            x=alt.X('Control_Type:N', title='Control Type', axis=alt.Axis(labelFontSize=12, titleFontSize=14)),
            y=alt.Y('Control_Quality_Score:Q', title='Average Quality Score', axis=alt.Axis(labelFontSize=12, titleFontSize=14)),
            color=alt.Color('Control_Type:N', scale=alt.Scale(range='plasma')), # Another color-blind friendly option
            tooltip=['Control_Type', alt.Tooltip('Control_Quality_Score', format='.1f')]
        ).properties(
            title={
                "text": "Average Control Quality Score by Control Type",
                "fontSize": 16,
                "anchor": "middle"
            }
        )
        st.subheader("Aggregated Comparison Plots")
        st.altair_chart(bar_chart_type, use_container_width=True)

        # Similar bar charts can be generated for 'Key_NonKey', 'Manual_Automated', 'Risk_Level'
    ```
    _Note on Trend Plot:_ The provided Jupyter Notebook content and synthetic data do not include a time-series dimension. Therefore, a time-based trend plot will not be included in this initial specification, focusing on the relationship and aggregated comparison plots explicitly supported by the notebook's data structure. If time-series analysis is required, the input data structure would need to be expanded to include a date/time column.

### 4.7 Displaying References

A dedicated section at the bottom of the application will list the provided references.

```python
# At the end of the Streamlit app:
st.markdown("---")
st.subheader("References:")
st.markdown("""
[1] "Control Assessment" and its sub-sections (e.g., "Controls contain the following attributes"), PRMIA Operational Risk Manager Handbook, Updated November, 2015. This section details the process of assessing control effectiveness and implementation quality, including control attributes.

[2] "Suggested Control Substantiation Methods by Attribute for High and Medium Risks" table on page 35, PRMIA Operational Risk Manager Handbook, Updated November, 2015. This table provides guidance on appropriate methods for control substantiation based on risk level and control attributes.
""")
```

### 4.8 Performance Optimization

*   `@st.cache_data` will be crucial for the `load_control_data_streamlit` function to prevent re-running data loading and initial processing on every interaction, significantly improving responsiveness.
*   The use of Pandas for data manipulation and Altair for charting is efficient for the expected dataset sizes (up to ~1000 records) and adheres to the open-source library constraint.

