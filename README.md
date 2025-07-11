# Control Effectiveness Evaluator

## 📊 Project Title and Description

The **Control Effectiveness Evaluator** is a Streamlit web application designed to assist in assessing the design and implementation quality of operational controls. This tool provides a structured approach to evaluate individual controls based on key attributes and allows for the analysis of larger datasets of control information.

Whether you're an auditor, risk manager, or operations professional, this application empowers you to:
*   Define characteristics of a single control and receive an immediate evaluation.
*   Calculate a quantitative **'Control Quality Score'** to gauge overall effectiveness.
*   Get suggestions for an appropriate **'Control Substantiation Method'** based on control attributes and associated risk.
*   Upload and analyze your own control data in CSV format, or generate synthetic data for testing and exploration.
*   Visualize key relationships within your control data to identify trends and potential areas for improvement.

The goal is to provide a user-friendly interface for understanding, evaluating, and managing the quality of operational controls within an organization.

## ✨ Features

*   **Interactive Control Evaluation**: Define attributes (Control Type, Key/Non-Key, Manual/Automated, Risk Level, Implementation Quality Rating) for a single control.
*   **Control Quality Score Calculation**: Dynamically calculates a "Control Quality Score" based on user-defined inputs for individual controls or batch data.
*   **Substantiation Method Suggestion**: Provides a recommended "Control Substantiation Method" (e.g., Re-performance, Examination, Inquiry) tailored to the control's characteristics and risk.
*   **Data Upload & Analysis**:
    *   Upload operational control data in CSV format.
    *   Generate synthetic control data for testing and demonstration purposes.
    *   Comprehensive data validation and preprocessing.
    *   Display of raw data and summary statistics (descriptive statistics, value counts).
*   **Interactive Visualizations**:
    *   Scatter plot showing the relationship between Implementation Frequency and Design Quality, colored by Control Type.
    *   Bar chart visualizing the average "Control Quality Score" by Control Type.
*   **Modular Navigation**: Easy-to-use sidebar navigation to switch between "Home," "Evaluate Control," and "Analyze Data" sections.

## 🚀 Getting Started

Follow these steps to get the application up and running on your local machine.

### Prerequisites

*   Python 3.7+
*   `pip` (Python package installer)

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/control-effectiveness-evaluator.git
    cd control-effectiveness-evaluator
    ```
    *(Replace `https://github.com/your-username/control-effectiveness-evaluator.git` with your actual repository URL)*

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    ```

3.  **Activate the virtual environment:**
    *   **On Windows:**
        ```bash
        .\venv\Scripts\activate
        ```
    *   **On macOS/Linux:**
        ```bash
        source venv/bin/activate
        ```

4.  **Install the required dependencies:**
    Create a `requirements.txt` file in the root directory of your project with the following content:

    ```
    streamlit==1.36.0
    pandas==2.2.2
    plotly==5.22.0
    ```
    Then, install them:
    ```bash
    pip install -r requirements.txt
    ```

## 🎮 Usage

1.  **Run the Streamlit application:**
    Ensure your virtual environment is activated and you are in the project's root directory (where `app.py` is located).
    ```bash
    streamlit run app.py
    ```

2.  **Access the application:**
    After running the command, your web browser will automatically open the application at `http://localhost:8501/` (or a similar address).

3.  **Navigate the app:**
    *   Use the **sidebar** to switch between the "Home", "Evaluate Control", and "Analyze Data" pages.
    *   On the **"Evaluate Control"** page, select control attributes and click "Calculate Score & Method" to see the results for a single control.
    *   On the **"Analyze Data"** page, you can either upload a CSV file containing your control data or check the "Generate synthetic data instead" box to create sample data. The application will then display the data table, summary statistics, and visualizations.

## 📁 Project Structure

The project follows a modular structure to organize different functionalities:

```
control-effectiveness-evaluator/
├── app.py
├── requirements.txt
├── application_pages/
│   ├── __init__.py
│   ├── home.py
│   ├── evaluate_control.py
│   └── analyze_data.py
└── (optional) calculate_control_quality_score.py # (Implied by imports in evaluate_control.py,
└── (optional) suggest_substantiation_method.py  # though definitions are in analyze_data.py in the provided code)
```

*   **`app.py`**: The main entry point of the Streamlit application. It sets up the page configuration, displays the main title, and handles navigation to different pages.
*   **`requirements.txt`**: Lists all the Python dependencies required to run the application.
*   **`application_pages/`**: A directory containing separate Python files for each major section/page of the application, promoting modularity and code organization.
    *   **`home.py`**: Contains the content and logic for the application's home page.
    *   **`evaluate_control.py`**: Handles the interactive input and calculation for evaluating a single control.
    *   **`analyze_data.py`**: Manages data loading (CSV upload or synthetic generation), validation, preprocessing, calculations for batch data, and generates visualizations. It also contains the core logic for `calculate_control_quality_score` and `suggest_substantiation_method` within its scope as provided in the snippet.
*   **`(optional) calculate_control_quality_score.py`**: (If refactored for cleaner imports) Contains the function to calculate the control quality score.
*   **`(optional) suggest_substantiation_method.py`**: (If refactored for cleaner imports) Contains the function to suggest the control substantiation method.

## 🛠 Technology Stack

*   **Python**: The core programming language used for the application.
*   **Streamlit**: The open-source app framework used to build interactive web applications purely in Python.
*   **Pandas**: A powerful library for data manipulation and analysis, used for handling CSV data and synthetic data generation.
*   **Plotly Express**: A high-level API for creating interactive, publication-quality visualizations with minimal code, used for data plotting.

## 🤝 Contributing

Contributions are welcome! If you have suggestions for improvements, new features, or bug fixes, please feel free to:

1.  Fork the repository.
2.  Create a new branch (`git checkout -b feature/YourFeature`).
3.  Make your changes and commit them (`git commit -m 'Add new feature'`).
4.  Push to the branch (`git push origin feature/YourFeature`).
5.  Open a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the `LICENSE` file for details (if you have one). If no explicit license file, you can state: "This project is open-source and available for use and modification. No formal license specified for this lab project."

## 📞 Contact

For any questions or inquiries, please open an issue on the GitHub repository or contact:

*   **Your Name/Lab Contact**: [Your Email Address / Your GitHub Profile Link]
*   **Quant University**: [https://www.quantuniversity.com/](https://www.quantuniversity.com/) (as per logo)
