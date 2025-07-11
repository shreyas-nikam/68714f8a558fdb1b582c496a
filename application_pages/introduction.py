
import streamlit as st

def run_introduction():
    st.header("Introduction to Control Effectiveness Evaluation")
    st.markdown("""
    This application provides a hands-on experience in defining and evaluating operational controls. It allows you to apply theoretical knowledge from the `PRMIA Operational Risk Manager Handbook` regarding control attributes and assessment methods.

    **Key Features:**

    *   Calculate a qualitative 'Control Quality Score' based on user inputs.
    *   Suggest a control substantiation method.
    *   Visualize relationships between control attributes and derived scores using a synthetic or uploaded dataset.

    **References:**

    [1] "Control Assessment" and its sub-sections (e.g., "Controls contain the following attributes"), PRMIA Operational Risk Manager Handbook, Updated November, 2015.

    [2] "Suggested Control Substantiation Methods by Attribute for High and Medium Risks" table on page 35, PRMIA Operational Risk Manager Handbook, Updated November, 2015.
    """)
