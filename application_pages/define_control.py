
import streamlit as st

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

def run_define_control():
    st.header("Define a Single Control")

    control_type = st.selectbox("Control Type", options=["Preventative", "Detective"], help="Select whether the control aims to prevent an issue before it occurs (Preventative) or detect it after (Detective).")
    key_nonkey = st.selectbox("Key/Non-Key", options=["Key", "Non-Key"], help="Indicate if this is a primary control (Key) or a supporting one (Non-Key).")
    manual_automated = st.selectbox("Manual/Automated", options=["Manual", "Automated"], help="Choose if the control is performed manually or by an automated system.")
    risk_level = st.selectbox("Risk Level", options=["High", "Medium", "Low"], help="Specify the inherent risk level associated with this control.")
    implementation_quality_rating = st.slider("Implementation Quality Rating", min_value=1, max_value=5, value=3, step=1, help="Rate the observed quality of the control's implementation (1: Poor, 5: Excellent).")

    if st.button("Calculate Control Quality and Suggest Method"):
        try:
            score = calculate_control_quality_score(control_type, key_nonkey, manual_automated, implementation_quality_rating)
            method = suggest_substantiation_method(control_type, key_nonkey, manual_automated, risk_level)

            st.subheader("Results:")
            st.metric("Control Quality Score", value=score)
            st.info(f"Suggested Substantiation Method: {method}")

        except ValueError as e:
            st.error(f"Error: {e}")
