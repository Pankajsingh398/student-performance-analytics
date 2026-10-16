# Student Performance Analytics & Prediction System

## Project overview
An interactive Python dashboard that explores student marks, attendance, and daily study hours. It includes summary metrics, charts, filtering, a CSV report download, and a transparent rule-based study-pattern estimate.

**Important:** The included student records are synthetic demo data. The estimate is educational and is not a validated machine-learning model or a guarantee of a student's future performance.

## Features
- Upload a CSV file or use the included sample dataset
- Average marks, pass percentage, total students, and high-risk count
- Marks distribution and attendance-vs-marks charts
- Rule-based risk labels (High / Medium / Low)
- Searchable-looking student table and downloadable CSV report
- Interactive study-pattern estimate
- Basic data cleaning for numeric columns and sensible ranges

## Technology used
- Python
- Streamlit
- Pandas
- NumPy
- Matplotlib

## Run locally
1. Install Python 3.10 or newer.
2. Extract the ZIP file and open a terminal in this folder.
3. Create a virtual environment (recommended):
   - Windows: `python -m venv .venv`
   - Activate: `.venv\\Scripts\\activate`
4. Install dependencies:
   `pip install -r requirements.txt`
5. Start the dashboard:
   `streamlit run app.py`
6. Your browser should open the local app. If not, open the local URL printed in the terminal.

## CSV format
Your uploaded CSV must include these columns:
`student_id, name, attendance, study_hours, marks`

Example:
`S001,Student 1,82,2.5,74`

- attendance: percentage from 0 to 100
- study_hours: study hours per day, zero or greater
- marks: score from 0 to 100

## Suggested project explanation for interview
"I built a Student Performance Analytics dashboard using Python. Pandas is used to clean and analyze records, NumPy creates rule-based performance labels, Matplotlib visualizes the data, and Streamlit provides an interactive web interface. Users can upload their own CSV, filter students, view performance patterns, and download a report. The risk labels are transparent rules for demonstration rather than a medically or academically validated prediction."

## Limitations and future scope
- Current demo dataset is synthetic.
- Risk categories use simple rules and should not be treated as an official academic decision.
- Future work: connect a database, add authentication, evaluate a machine-learning model using a real consented dataset, and export PDF reports.
