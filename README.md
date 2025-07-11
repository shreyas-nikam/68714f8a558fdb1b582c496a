Here's a comprehensive `README.md` file for your Streamlit application lab project, incorporating all the requested sections and detailing the application's functionality based on your provided code.

---

# QuLab: Operational Control Effectiveness Evaluation Streamlit Application

![QuLab Logo](https://www.quantuniversity.com/assets/img/logo5.jpg)

## Project Title and Description

**QuLab** is an interactive Streamlit application designed as a lab project to explore and demonstrate the principles of operational control effectiveness evaluation. Leveraging concepts from the PRMIA Operational Risk Manager Handbook, this application provides tools for defining individual controls, calculating their quality scores, suggesting appropriate substantiation methods, and analyzing datasets of controls through interactive visualizations. It aims to provide a hands-on experience for understanding key attributes that contribute to a control's effectiveness and how they relate to assessment methodologies.

## Features

This application offers the following key functionalities:

*   **Interactive Introduction**: Provides an overview of control effectiveness evaluation and the application's capabilities, referencing the PRMIA Operational Risk Manager Handbook.
*   **Single Control Definition & Evaluation**:
    *   Allows users to define a single operational control by selecting its type (Preventative/Detective), key/non-key status, manual/automated nature, inherent risk level, and implementation quality rating.
    *   Dynamically calculates a qualitative 'Control Quality Score' based on the selected attributes.
    *   Suggests a relevant 'Control Substantiation Method' (e.g., Re-performance, Examination, Inquiry) based on the control's characteristics and associated risk level, following PRMIA guidelines.
*   **Control Dataset Analysis**:
    *   **Flexible Data Source**: Supports uploading your own control dataset via a CSV file or generating a synthetic dataset for quick experimentation.
    *   **Automated Calculations**: Automatically calculates 'Control Quality Scores' and 'Suggested Substantiation Methods' for all controls in the loaded dataset.
    *   **Robust Data Validation**: Includes validation checks for required columns, data types, and presence of missing/duplicate values to ensure data integrity.
    *   **Interactive Filtering**: Enables users to filter the dataset by various control attributes (Type, Key/Non-Key, Manual/Automated, Risk Level, Implementation Frequency, Design Quality Rating).
    *   **Dynamic Visualizations**: Generates insightful Plotly charts to visualize relationships between control attributes, derived scores, and effectiveness, including:
        *   Scatter plot showing Control Quality vs. Implementation & Design Quality.
        *   Bar charts comparing average Control Quality Scores by Control Type and Risk Level.
    *   **Data Display**: Presents the raw and filtered data in interactive tables.

## Getting Started

Follow these instructions to get a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

*   Python 3.7+
*   `pip` (Python package installer)

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/yourusername/QuLab-Control-Effectiveness.git
    cd QuLab-Control-Effectiveness
    ```
    *(Note: Replace `https://github.com/yourusername/QuLab-Control-Effectiveness.git` with the actual repository URL if this is hosted publicly.)*

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

4.  **Install the required Python packages:**
    ```bash
    pip install -r requirements.txt
    ```
    *(If `requirements.txt` is not provided in the clone, manually create one in the root directory with the following content and then run `pip install -r requirements.txt`)*:

    **`requirements.txt`:**
    ```
    streamlit>=1.0
    pandas>=1.0
    plotly>=5.0
    ```

## Usage

To run the application, navigate to the project's root directory in your terminal (where `app.py` is located) and execute the following command:

```bash
streamlit run app.py
```

This will open the application in your default web browser (usually at `http://localhost:8501`).

### Basic Usage Instructions:

1.  **Navigation**: Use the sidebar on the left to navigate between the three main pages: "Introduction", "Define a Single Control", and "Analyze Control Dataset".

2.  **Introduction Page**:
    *   Provides an overview and context for the application.

3.  **Define a Single Control Page**:
    *   Use the dropdown menus and slider to select the attributes for a hypothetical control.
    *   Click the "Calculate Control Quality and Suggest Method" button to see the results.

4.  **Analyze Control Dataset Page**:
    *   **Data Source Selection**: In the sidebar, choose between "Upload CSV File" or "Generate Synthetic Data".
        *   **Upload CSV File**: Click "Browse files" to upload your own CSV.
            *   **Required CSV Columns**: Your CSV file must contain the following columns with appropriate data types:
                *   `Control_Type` (string: "Preventative", "Detective")
                *   `Key_NonKey` (string: "Key", "Non-Key")
                *   `Manual_Automated` (string: "Manual", "Automated")
                *   `Risk_Level` (string: "High", "Medium", "Low")
                *   `Implementation_Frequency` (numeric: 1-5, used as rating for quality)
                *   `Design_Quality_Rating` (numeric: 1-5)
                *   `Control_ID` (string: unique identifier for each control)
        *   **Generate Synthetic Data**: Enter the desired number of synthetic records and click "Generate Data".
    *   **Data Validation & Processing**: The application will validate the loaded data and then calculate the 'Control Quality Score' and 'Suggested Substantiation Method' for each record.
    *   **Filtering**: Use the multiselect and slider widgets in the sidebar to dynamically filter the displayed data and visualizations based on control attributes.
    *   **Visualizations**: Explore the generated scatter and bar charts to gain insights into your control dataset.

## Project Structure

The project is organized as follows:

```
QuLab-Control-Effectiveness/
├── app.py
├── requirements.txt
├── README.md
└── application_pages/
    ├── __init__.py
    ├── introduction.py
    ├── define_control.py
    └── analyze_dataset.py
```

*   `app.py`: The main Streamlit application entry point. Handles overall layout and navigation.
*   `requirements.txt`: Lists all Python dependencies required to run the application.
*   `README.md`: This file, providing project information.
*   `application_pages/`: A directory containing the code for each distinct page of the Streamlit application.
    *   `introduction.py`: Implements the content for the "Introduction" page.
    *   `define_control.py`: Implements the logic and UI for the "Define a Single Control" page.
    *   `analyze_dataset.py`: Implements the data loading, processing, analysis, and visualization for the "Analyze Control Dataset" page.

## Technology Stack

*   **Python**: The core programming language.
*   **Streamlit**: The framework used for building the interactive web application.
*   **Pandas**: Essential for data manipulation and analysis, especially in the dataset analysis section.
*   **Plotly**: Used for generating interactive and visually appealing data visualizations.

## Contributing

Contributions are welcome! If you have suggestions for improvements, new features, or bug fixes, please follow these steps:

1.  Fork the repository.
2.  Create a new branch (`git checkout -b feature/your-feature-name` or `bugfix/issue-description`).
3.  Make your changes and ensure your code adheres to good practices.
4.  Commit your changes (`git commit -m 'feat: Add new feature'` or `fix: Resolve bug`).
5.  Push to your branch (`git push origin feature/your-feature-name`).
6.  Open a Pull Request to the `main` branch of this repository.

Please also feel free to open an issue if you encounter any bugs or have feature requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
*(Note: You should create a `LICENSE` file in the root of your project with the MIT license text if you don't have one already.)*

## Contact

For questions or feedback, please reach out to the project maintainers:

*   **QuantUniversity**:
    *   Website: [www.quantuniversity.com](https://www.quantuniversity.com)
    *   Email: [info@quantuniversity.com](mailto:info@quantuniversity.com)

---