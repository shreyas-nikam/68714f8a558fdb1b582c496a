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
    import pandas as pd
    import random

    control_types = ["Preventative", "Detective"]
    key_nonkey_options = ["Key", "Non-Key"]
    manual_automated_options = ["Manual", "Automated"]
    risk_level_options = ["High", "Medium", "Low"]
    implementation_quality_ratings = [1, 2, 3, 4, 5]

    data = {
        "Control_Type": [random.choice(control_types) for _ in range(num_records)],
        "Key_NonKey": [random.choice(key_nonkey_options) for _ in range(num_records)],
        "Manual_Automated": [random.choice(manual_automated_options) for _ in range(num_records)],
        "Risk_Level": [random.choice(risk_level_options) for _ in range(num_records)],
        "Implementation_Quality_Rating": [random.choice(implementation_quality_ratings) for _ in range(num_records)],
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
        df = generate_synthetic_control_data(num_records)
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
    
    # Move the slider to sidebar
    with st.sidebar:
        st.divider()
        st.subheader("Data Generation Settings")
        num_records = st.slider("Number of records", min_value=5, max_value=1000, value=100, 
                           help="Number of synthetic control records to generate. Adjust for performance.")
        st.info("Using synthetic data for analysis")
    
    # Create fresh synthetic data when the slider changes
    if 'previous_num_records' not in st.session_state or st.session_state.previous_num_records != num_records:
        df = generate_synthetic_control_data(num_records)
        df['Implementation_Frequency'] = [random.randint(1, 5) for _ in range(num_records)]
        df['Design_Quality_Rating'] = [random.randint(1, 5) for _ in range(num_records)]
        df['Control_ID'] = [f'CTRL_{i:03d}' for i in range(1, num_records + 1)]
        st.session_state.previous_num_records = num_records
        st.session_state.current_df = df
    else:
        df = st.session_state.current_df
    
    if df is not None:
        df = validate_and_preprocess_data(df)

    if df is not None and not df.empty:
        # Calculate Control Quality Score first
        try:
            df['Control_Quality_Score'] = df.apply(lambda row: calculate_control_quality_score(row['Control_Type'], row['Key_NonKey'], row['Manual_Automated'], row['Implementation_Frequency']), axis=1)
        except Exception as e:
            st.error(f"Error calculating Control Quality Score: {e}")

        # Show visualizations first
        st.subheader("Data Analysis")

        # After visualizations, show the data table
        st.subheader("Data Table")
        with st.expander("View Raw Data"):
            st.dataframe(df, use_container_width=True)
        
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
            
            control_counts = df['Control_Type'].value_counts()
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
            
            risk_counts = df['Risk_Level'].value_counts()
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
            
            avg_scores = df.groupby('Control_Type')['Control_Quality_Score'].mean().reset_index()
            fig_quality = px.bar(
                avg_scores,
                x='Control_Type',
                y='Control_Quality_Score',
                title="Average Control Quality Score by Type",
                labels={"Control_Quality_Score": "Average Quality Score"},
                color='Control_Type',
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
            
            automation_counts = df['Manual_Automated'].value_counts()
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
            
            key_counts = df['Key_NonKey'].value_counts()
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
                avg_quality = df['Control_Quality_Score'].mean()
                st.metric(
                    "Average Control Quality", 
                    f"{avg_quality:.2f}",
                    help="Higher scores indicate more robust controls (Range: 1-15)"
                )
                
            with col2:
                high_risk_count = len(df[df['Risk_Level'] == 'High'])
                high_risk_pct = (high_risk_count / len(df)) * 100
                st.metric(
                    "High Risk Controls", 
                    f"{high_risk_count} ({high_risk_pct:.1f}%)",
                    help="Number and percentage of high-risk controls requiring intensive monitoring"
                )
                
            with col3:
                automated_count = len(df[df['Manual_Automated'] == 'Automated'])
                automation_rate = (automated_count / len(df)) * 100
                st.metric(
                    "Automation Rate", 
                    f"{automation_rate:.1f}%",
                    help="Percentage of controls that are automated (higher is generally better)"
                )
                
            with col4:
                key_controls = len(df[df['Key_NonKey'] == 'Key'])
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
            preventative_pct = (len(df[df['Control_Type'] == 'Preventative']) / total_controls) * 100
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

        # Ensure all rows are read from the dataset
        if df.shape[0] < 100:
            st.warning("The dataset contains fewer rows than expected. Please check the file or preprocessing steps.")
