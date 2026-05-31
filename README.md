# Python Assignment: Ideal Function Mapping System (Python + SQL + ML + Visualization)

## Project Overview

This project implements a complete data pipeline that maps **test data points to ideal mathematical functions** using statistical analysis and machine learning techniques.

The system:
- Loads datasets from CSV files
- Stores and manages data using a SQLite database (SQLAlchemy ORM)
- Finds best-fit functions using Mean Squared Error (MSE)
- Maps unseen test data to ideal functions
- Identifies outliers based on deviation thresholds
- Visualizes datasets using Bokeh
- Includes unit testing for validation

---

## Objective

To identify the most suitable ideal function for each training dataset column and use it to map test data points with minimal deviation, ensuring accurate functional approximation.

---

## Methodology

### 1. Data Loading
- Training, Test, and Ideal datasets are loaded from CSV files.
- Data is validated using custom exception handling.

### 2. Database Integration
- SQLAlchemy ORM is used to:
  - Store training data
  - Store ideal functions
  - Store mapped test results

### 3. Best Fit Function Selection
- Mean Squared Error (MSE) is calculated between:
  - Training data columns (y1–y4)
  - Ideal function columns (y1–y50)
- The function with the lowest error is selected.

### 4. Test Data Mapping
- Each test point is compared with selected ideal functions.

### 5. Outlier Detection
- Points that do not satisfy mapping conditions are classified as outliers

### 6. Visualization
- Bokeh is used for interactive visualization of:
  - Training data
  - Ideal functions
  - Test data
  - Outliers

## Project Structure
Project Folder:
- train.csv
- test.csv
- ideal.csv
- python.ipynb
- ideal_function_mapping.py
- .gitignore
- requirements.txt
- README.md

## Technologies Used
- Python
- Pandas
- NumPy
- SQLAlchemy (ORM)
- SQLite
- Scikit-learn (MSE calculation)
- Bokeh (visualization)
- Unittest (testing)

## How to Run the Project

Step 1: Install dependencies
```bash
pip install -r requirements.txt

Step 2: Run the notebook
Open: python.ipynb
Or run in Jupyter Notebook / VS Code

Step 3: Run tests
python -m unittest discover

Output
Best-fit ideal function mapping
Test data classification (mapped vs outliers)
Database-stored results
Interactive Bokeh graphs

Author
Nuzki J
GitHub: https://github.com/NuzkiJ
