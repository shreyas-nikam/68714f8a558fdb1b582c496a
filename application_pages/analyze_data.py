import streamlit as st
import pandas as pd
import plotly.express as px
import random

def generate_synthetic_control_data(num_records):
    """
    Generates synthetic control data for simulation purposes.

    Args:
        num_records (int): Number of records to generate.

    Returns:
        pd.DataFrame: A DataFrame containing synthetic control data.
    """
    control_types = ["Preventative", "Detective"]
    key_nonkey_options = ["Key", "Non-Key"]
    manual_automated_options = ["Manual", "Automated"]
    risk_level_options = ["High", "Medium", "Low"]
    implementation_quality_ratings = [1, 2, 3, 4, 5]

    data = {
        "Control Type": [random.choice(control_types) for _ in range(num_records)],
        "Key/Non-Key": [random.choice(key_nonkey_options) for _ in range(num_records)],
        "Manual/Automated": [random.choice(manual_automated_options) for _ in range(num_records)],
        "Risk Level": [random.choice(risk_level_options) for _ in range(num_records)],
        "Implementation Quality Rating": [random.choice(implementation_quality_ratings) for _ in range(num_records)],
        "Implementation Frequency": [random.randint(1, 5) for _ in range(num_records)],
        "Design Quality Rating": [random.randint(1, 5) for _ in range(num_records)],
        "Control ID": [f'CTRL_{i:03d}' for i in range(1, num_records + 1)]
    }

    return pd.DataFrame(data)

def validate_uploaded_data(df):
    """
    Validates the uploaded dataset for required columns and data types.
    
    Args:
        df (pd.DataFrame): The uploaded dataframe to validate
    
    Returns:
        tuple: (is_valid, error_messages, df_processed)
    """
    if df is None or df.empty:
        return False, ["Dataset is empty"], None
    
    # Required columns and their expected data types
    required_columns = {
        'Control Type': 'categorical',
        'Key/Non-Key': 'categorical', 
        'Manual/Automated': 'categorical',
        'Risk Level': 'categorical',
        'Implementation Quality Rating': 'numeric',
        'Implementation Frequency': 'numeric',
        'Design Quality Rating': 'numeric',
        'Control ID': 'string'
    }
    
    # Expected values for categorical columns
    expected_values = {
        'Control Type': ['Preventative', 'Detective'],
        'Key/Non-Key': ['Key', 'Non-Key'],
        'Manual/Automated': ['Manual', 'Automated'],
        'Risk Level': ['High', 'Medium', 'Low']
    }
    
    error_messages = []
    df_processed = df.copy()
    
    # Check for missing required columns
    missing_columns = [col for col in required_columns.keys() if col not in df.columns]
    if missing_columns:
        error_messages.append(f"Missing required columns: {', '.join(missing_columns)}")
        return False, error_messages, None
    
    # Validate each column
    for col, data_type in required_columns.items():
        if col not in df.columns:
            continue
            
        # Check for null values
        null_count = df[col].isnull().sum()
        if null_count > 0:
            error_messages.append(f"Column '{col}' contains {null_count} null values")
        
        # Validate data types and values
        if data_type == 'numeric':
            # Try to convert to numeric
            try:
                df_processed[col] = pd.to_numeric(df[col], errors='coerce')
                if df_processed[col].isnull().any():
                    invalid_count = df_processed[col].isnull().sum() - null_count
                    if invalid_count > 0:
                        error_messages.append(f"Column '{col}' contains {invalid_count} non-numeric values")
                
                # Check range for rating columns
                if 'Rating' in col or 'Frequency' in col:
                    valid_range = df_processed[col].between(1, 5, inclusive='both')
                    if not valid_range.all():
                        invalid_range_count = (~valid_range).sum()
                        error_messages.append(f"Column '{col}' contains {invalid_range_count} values outside range 1-5")
            except:
                error_messages.append(f"Column '{col}' cannot be converted to numeric")
        
        elif data_type == 'categorical':
            # Check if values are in expected categories
            if col in expected_values:
                invalid_values = df[col][~df[col].isin(expected_values[col])].unique()
                if len(invalid_values) > 0:
                    error_messages.append(f"Column '{col}' contains invalid values: {list(invalid_values)}. Expected: {expected_values[col]}")
        
        elif data_type == 'string':
            # Check for duplicate Control_IDs
            if col == 'Control ID':
                duplicate_count = df[col].duplicated().sum()
                if duplicate_count > 0:
                    error_messages.append(f"Column '{col}' contains {duplicate_count} duplicate values")
    
    # Additional business logic validations
    if len(error_messages) == 0:
        # Check minimum number of records
        if len(df) < 5:
            error_messages.append("Dataset must contain at least 5 records")
        
        # Check maximum number of records for performance
        if len(df) > 10000:
            error_messages.append("Dataset contains too many records (max 10,000). Please reduce dataset size.")
    
    is_valid = len(error_messages) == 0
    return is_valid, error_messages, df_processed if is_valid else None

def display_sample_template():
    """Display a sample template for users to understand the required format."""
    st.markdown("""
    ### Sample Data Template
    
    Below is a sample template showing the exact format required for your dataset:
    """)
    
    # Generate a small sample for display
    sample_data = generate_synthetic_control_data(5)
    st.dataframe(sample_data, use_container_width=True)
    
    st.markdown("""
    **Column Requirements:**
    
    | **Column Name** | **Data Type** | **Valid Values** | **Description** |
    |-----------------|---------------|------------------|-----------------|
    | `Control Type` | Text | Preventative, Detective | Type of control |
    | `Key/Non-Key` | Text | Key, Non-Key | Control classification |
    | `Manual/Automated` | Text | Manual, Automated | Execution method |
    | `Risk Level` | Text | High, Medium, Low | Associated risk level |
    | `Implementation Quality Rating` | Number | 1-5 | Quality rating |
    | `Implementation Frequency` | Number | 1-5 | Frequency rating |
    | `Design Quality Rating` | Number | 1-5 | Design rating |
    | `Control ID` | Text | Unique values | Control identifier |
    
    **Important Notes:**
    - File format: CSV (.csv)
    - Minimum 5 records, maximum 10,000 records
    - No missing values allowed
    - Control ID values must be unique
    - All numeric values must be between 1-5
    - Use exact column names as shown above (including spaces and special characters)
    """)

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
    
    # Data source selection
    st.subheader("Data Source Selection")
    
    data_source = st.radio(
        "Choose your data source:",
        options=["Generate Synthetic Data", "Upload Your Own Dataset"],
        help="Select whether to use synthetic data for exploration or upload your own control dataset"
    )
    
    df = None
    
    if data_source == "Generate Synthetic Data":
        # Move the slider to sidebar for synthetic data
        with st.sidebar:
            st.divider()
            st.subheader("Data Generation Settings")
            num_records = st.slider("Number of records", min_value=5, max_value=1000, value=100, 
                               help="Number of synthetic control records to generate. Adjust for performance.")
            
            st.info("Using synthetic data for analysis")
        
        # Create fresh synthetic data when the slider changes
        if 'previous_num_records' not in st.session_state or st.session_state.previous_num_records != num_records:
            df = generate_synthetic_control_data(num_records)
            st.session_state.previous_num_records = num_records
            st.session_state.current_df = df
        else:
            df = st.session_state.current_df
            
        st.success(f"Generated {num_records} synthetic control records for analysis")
    
    else:  # Upload Your Own Dataset
        st.markdown("### File Upload")
        
        # Provide sample template download first
        st.markdown("**Step 1: Download Sample Template**")
        st.markdown("Download the sample template below, edit it with your data, and upload it back:")
        
        # Generate sample template with more records for better example
        sample_template = generate_synthetic_control_data(20)
        csv_template = sample_template.to_csv(index=False)
        
        col1, col2 = st.columns([1, 3])
        with col1:
            st.download_button(
                label="Download Sample Template",
                data=csv_template,
                file_name="control_data_template.csv",
                mime="text/csv",
                help="Download this sample CSV file, edit it with your data, and upload it back"
            )
        
        with col2:
            st.info("The template contains 20 sample records. Replace them with your actual control data while keeping the exact column names and format.")
        
        # Show expandable template preview
        with st.expander("View Sample Template Format", expanded=False):
            display_sample_template()
        
        st.divider()
        
        # File uploader
        st.markdown("**Step 2: Upload Your Data File**")
        uploaded_file = st.file_uploader(
            "Upload your control data file (CSV format)",
            type=['csv'],
            help="Upload the CSV file with your control data. Make sure it follows the template format exactly."
        )
        
        if uploaded_file is not None:
            try:
                # Read the uploaded file
                df_uploaded = pd.read_csv(uploaded_file)
                
                st.info(f"File uploaded successfully: {uploaded_file.name} ({len(df_uploaded)} records)")
                
                # Validate the uploaded data
                with st.spinner("Validating your dataset..."):
                    is_valid, error_messages, df_processed = validate_uploaded_data(df_uploaded)
                
                if is_valid:
                    st.success("Dataset validation passed! Your data is ready for analysis.")
                    df = df_processed
                    
                    # Show a preview of the data
                    with st.expander("Preview of Your Data", expanded=False):
                        st.dataframe(df.head(10), use_container_width=True)
                        st.caption(f"Showing first 10 rows of {len(df)} total records")
                else:
                    st.error("Dataset validation failed. Please fix the following issues:")
                    
                    for i, error in enumerate(error_messages, 1):
                        st.error(f"{i}. {error}")
                    
                    st.markdown("### How to Fix These Issues:")
                    
                    # Provide specific guidance based on error types
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("""
                        **Common Issues & Solutions:**
                        1. **Wrong column names**: Use exact names from template
                        2. **Missing values**: Fill all empty cells
                        3. **Invalid categories**: Use only allowed values
                        4. **Number format**: Ensure ratings are 1-5
                        5. **Duplicate IDs**: Make Control ID values unique
                        """)
                    
                    with col2:
                        st.markdown("""
                        **Quick Fixes:**
                        - Download the template again
                        - Copy your data carefully
                        - Check spelling and capitalization
                        - Remove any extra columns
                        - Ensure no blank rows
                        """)
                    
                    # Show the uploaded data structure for debugging
                    st.markdown("### Your Uploaded Data Structure:")
                    st.write(f"**Columns found:** {list(df_uploaded.columns)}")
                    st.write(f"**Number of rows:** {len(df_uploaded)}")
                    
                    # Show first few rows to help identify issues
                    st.markdown("**First 5 rows of your data:**")
                    st.dataframe(df_uploaded.head(), use_container_width=True)
                    
                    return  # Stop execution if validation fails
                    
            except Exception as e:
                st.error(f"Error reading file: {str(e)}")
                st.info("Please ensure your file is a valid CSV format and try again.")
                st.markdown("""
                **Common file issues:**
                - File is not in CSV format
                - File is corrupted
                - Special characters in data
                - Encoding issues
                
                **Try this:** Save your Excel file as CSV and upload again.
                """)
                return
        
        else:
            st.info("Please upload a CSV file to begin analysis")
            return
    
    # Continue with analysis only if we have valid data
    if df is not None and not df.empty:
        # Calculate Control Quality Score
        try:
            df['Control Quality Score'] = df.apply(
                lambda row: calculate_control_quality_score(
                    row['Control Type'], 
                    row['Key/Non-Key'], 
                    row['Manual/Automated'], 
                    row['Implementation Quality Rating']
                ), axis=1
            )
        except Exception as e:
            st.error(f"Error calculating Control Quality Score: {e}")
            return

        # Show data summary
        st.divider()
        st.subheader("Dataset Summary")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Controls", len(df))
        with col2:
            st.metric("Avg Quality Score", f"{df['Control Quality Score'].mean():.2f}")
        with col3:
            high_risk_pct = (len(df[df['Risk Level'] == 'High']) / len(df)) * 100
            st.metric("High Risk %", f"{high_risk_pct:.1f}%")
        with col4:
            automation_pct = (len(df[df['Manual/Automated'] == 'Automated']) / len(df)) * 100
            st.metric("Automation %", f"{automation_pct:.1f}%")

        # Show visualizations
        st.subheader("Data Analysis")

        # Data table with option to view
        st.subheader("Data Table")
        with st.expander("View Complete Dataset"):
            st.dataframe(df, use_container_width=True)
            
            # Download processed data option
            csv_data = df.to_csv(index=False)
            st.download_button(
                label="Download Processed Data",
                data=csv_data,
                file_name="processed_control_data.csv",
                mime="text/csv",
                help="Download the processed dataset with calculated scores"
            )
        
        try:
            # 1. Control Types Distribution Chart
            st.subheader("Control Types Distribution")
            st.markdown("""
            **What this chart shows:** The distribution of Preventative vs Detective controls in your dataset.
            
            **Key insights:**
            - **Preventative controls** are designed to prevent issues before they occur (e.g., authorization requirements, segregation of duties)
            - **Detective controls** identify issues after they happen (e.g., reconciliations, monitoring reports)
            - A balanced portfolio typically has more preventative controls, but the optimal mix depends on your risk appetite
            """)
            
            control_counts = df['Control Type'].value_counts()
            fig_bar = px.bar(
                x=control_counts.index,
                y=control_counts.values,
                title="Distribution of Control Types",
                labels={"x": "Control Type", "y": "Count"},
                color=control_counts.index,
                color_discrete_map={'Preventative': '#2E8B57', 'Detective': '#4682B4'}
            )
            fig_bar.update_layout(showlegend=False)
            st.plotly_chart(fig_bar, use_container_width=True)

            # 2. Risk Level Distribution Chart
            st.subheader("Risk Level Distribution")
            st.markdown("""
            **What this chart shows:** The proportion of controls categorized by risk level across your control environment.
            
            **Key insights:**
            - **High Risk** controls require more rigorous testing and monitoring due to their critical nature
            - **Medium Risk** controls need regular attention but with less intensive procedures
            - **Low Risk** controls can often be tested less frequently or with lighter procedures
            - An organization with many high-risk controls may need to invest more in control strengthening
            """)
            
            risk_counts = df['Risk Level'].value_counts()
            fig_pie = px.pie(
                values=risk_counts.values,
                names=risk_counts.index,
                title="Risk Level Distribution",
                color_discrete_map={'High': '#DC143C', 'Medium': '#FF8C00', 'Low': '#32CD32'}
            )
            st.plotly_chart(fig_pie, use_container_width=True)

            # 3. Control Quality Score Analysis
            st.subheader("Average Control Quality Score by Type")
            st.markdown("""
            **What this chart shows:** The average Control Quality Score for each control type, helping identify which controls are performing better.
            
            **How Quality Score is calculated:**
            - **Control Type:** Preventative (+5 points) vs Detective (+2 points)
            - **Key vs Non-Key:** Key controls (+3 points) vs Non-Key (+1 point)
            - **Automation:** Automated (+2 points) vs Manual (+1 point)
            - **Implementation Quality:** Rating from 1-5 (adds 0-4 points)
            
            **Key insights:**
            - Higher scores indicate more robust and reliable controls
            - Preventative controls typically score higher due to their proactive nature
            - Scores help prioritize improvement efforts and resource allocation
            """)
            
            avg_scores = df.groupby('Control Type')['Control Quality Score'].mean().reset_index()
            fig_quality = px.bar(
                avg_scores,
                x='Control Type',
                y='Control Quality Score',
                title="Average Control Quality Score by Type",
                labels={"Control Quality Score": "Average Quality Score"},
                color='Control Type',
                color_discrete_map={'Preventative': '#2E8B57', 'Detective': '#4682B4'}
            )
            fig_quality.update_layout(showlegend=False)
            st.plotly_chart(fig_quality, use_container_width=True)

            # 4. Manual vs Automated Controls Distribution
            st.subheader("Manual vs Automated Controls")
            st.markdown("""
            **What this chart shows:** The split between manual and automated controls in your environment.
            
            **Key insights:**
            - **Automated controls** are generally more reliable and less prone to human error
            - **Manual controls** offer flexibility but require more oversight and training
            - Higher automation rates typically indicate a more mature control environment
            - Consider automation opportunities for high-frequency or error-prone manual controls
            """)
            
            automation_counts = df['Manual/Automated'].value_counts()
            fig_automation = px.pie(
                values=automation_counts.values,
                names=automation_counts.index,
                title="Manual vs Automated Controls Distribution",
                color_discrete_map={'Automated': '#4CAF50', 'Manual': '#FF9800'}
            )
            st.plotly_chart(fig_automation, use_container_width=True)

            # 5. Key vs Non-Key Controls Analysis
            st.subheader("Key vs Non-Key Controls")
            st.markdown("""
            **What this chart shows:** The distribution of key controls versus non-key controls.
            
            **Key insights:**
            - **Key controls** are critical for preventing or detecting material misstatements
            - **Non-Key controls** provide additional layers of protection but are less critical
            - Key controls require more rigorous testing and monitoring procedures
            - A balanced approach ensures comprehensive coverage without over-testing
            """)
            
            key_counts = df['Key/Non-Key'].value_counts()
            fig_key = px.bar(
                x=key_counts.index,
                y=key_counts.values,
                title="Key vs Non-Key Controls Distribution",
                labels={"x": "Control Classification", "y": "Count"},
                color=key_counts.index,
                color_discrete_map={'Key': '#E91E63', 'Non-Key': '#9C27B0'}
            )
            fig_key.update_layout(showlegend=False)
            st.plotly_chart(fig_key, use_container_width=True)

            # Key metrics in a clean layout
            st.subheader("Key Performance Indicators")
            st.markdown("""
            **Summary metrics** that provide quick insights into your control environment's overall health and characteristics.
            """)
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                avg_quality = df['Control Quality Score'].mean()
                st.metric(
                    "Average Control Quality", 
                    f"{avg_quality:.2f}",
                    help="Higher scores indicate more robust controls (Range: 1-15)"
                )
                
            with col2:
                high_risk_count = len(df[df['Risk Level'] == 'High'])
                high_risk_pct = (high_risk_count / len(df)) * 100
                st.metric(
                    "High Risk Controls", 
                    f"{high_risk_count} ({high_risk_pct:.1f}%)",
                    help="Number and percentage of high-risk controls requiring intensive monitoring"
                )
                
            with col3:
                automated_count = len(df[df['Manual/Automated'] == 'Automated'])
                automation_rate = (automated_count / len(df)) * 100
                st.metric(
                    "Automation Rate", 
                    f"{automation_rate:.1f}%",
                    help="Percentage of controls that are automated (higher is generally better)"
                )
                
            with col4:
                key_controls = len(df[df['Key/Non-Key'] == 'Key'])
                key_control_pct = (key_controls / len(df)) * 100
                st.metric(
                    "Key Controls", 
                    f"{key_controls} ({key_control_pct:.1f}%)",
                    help="Number and percentage of key controls critical for risk mitigation"
                )

            # Additional insights and recommendations
            st.subheader("Insights & Recommendations")
            
            # Calculate some insights
            total_controls = len(df)
            preventative_pct = (len(df[df['Control Type'] == 'Preventative']) / total_controls) * 100
            detective_pct = 100 - preventative_pct
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### **Control Mix Analysis**")
                if preventative_pct > 60:
                    st.success(f"Good preventative control coverage ({preventative_pct:.1f}%)")
                elif preventative_pct > 40:
                    st.warning(f"Moderate preventative control coverage ({preventative_pct:.1f}%)")
                else:
                    st.error(f"Low preventative control coverage ({preventative_pct:.1f}%)")
                
                if automation_rate > 50:
                    st.success(f"Good automation rate ({automation_rate:.1f}%)")
                else:
                    st.info(f"Consider increasing automation ({automation_rate:.1f}% current)")
            
            with col2:
                st.markdown("#### **Risk Profile**")
                if high_risk_pct > 30:
                    st.warning(f"High proportion of high-risk controls ({high_risk_pct:.1f}%)")
                    st.info("Consider control strengthening initiatives")
                else:
                    st.success(f"Balanced risk profile ({high_risk_pct:.1f}% high-risk)")
                
                if avg_quality < 8:
                    st.warning("Below average control quality - focus on improvements")
                elif avg_quality > 10:
                    st.success("Strong overall control quality")
                else:
                    st.info("Moderate control quality - room for enhancement")

        except Exception as e:
            st.error(f"Error creating visualizations: {e}")
