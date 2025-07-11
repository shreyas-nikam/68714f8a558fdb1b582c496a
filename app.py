
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
