
import streamlit as st
from application_pages.analyze_data import calculate_control_quality_score, suggest_substantiation_method

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

            control_quality_score = calculate_control_quality_score(control_type, key_nonkey, manual_automated, implementation_quality_rating)
            substantiation_method = suggest_substantiation_method(control_type, key_nonkey, manual_automated, risk_level)

            st.metric("Control Quality Score", value=control_quality_score)
            st.write(f"Suggested Substantiation Method: {substantiation_method}")
        except Exception as e:
            st.error(f"An error occurred: {e}")
