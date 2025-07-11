
import streamlit as st
st.set_page_config(page_title="QuLab", layout="wide")
st.sidebar.image("https://www.quantuniversity.com/assets/img/logo5.jpg")
st.sidebar.divider()
st.title("QuLab")
st.divider()
st.markdown("""
In this lab, we will explore the concept of control effectiveness evaluation using a Streamlit application. This application provides tools for defining and analyzing operational controls, calculating control quality scores, and suggesting appropriate substantiation methods.

The application is divided into three main pages:

*   **Page 1: Introduction** - Provides an overview of control effectiveness evaluation and the application's features.
*   **Page 2: Define a Single Control** - Allows users to define a single control and calculate its quality score and suggested substantiation method.
*   **Page 3: Analyze Control Dataset** - Enables users to upload or generate a dataset of controls and analyze their effectiveness through visualizations and data tables.
""")

page = st.sidebar.selectbox(label="Navigation", options=["Introduction", "Define a Single Control", "Analyze Control Dataset"])

if page == "Introduction":
    from application_pages.introduction import run_introduction
    run_introduction()
elif page == "Define a Single Control":
    from application_pages.define_control import run_define_control
    run_define_control()
elif page == "Analyze Control Dataset":
    from application_pages.analyze_dataset import run_analyze_dataset
    run_analyze_dataset()
