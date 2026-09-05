# 🤖 AI Data Cleaning Assistant

An AI-powered data quality and cleaning application built with Python and Streamlit.

The application automatically analyzes uploaded CSV/Excel datasets, identifies data quality issues and anomalies, provides AI-powered recommendations, cleans the dataset, and allows users to export the cleaned data and audit logs.

## 🚀 Features

- 📂 CSV and Excel file upload
- 🔍 Automated data profiling
- ⚠️ Data quality issue detection
- 📊 Missing-value analysis
- 🔁 Duplicate detection
- 🚨 Anomaly detection
- 🤖 AI-powered data quality recommendations
- 🧹 Automated data cleaning
- 📈 Before/after data quality comparison
- 📝 Cleaning audit log
- 📥 Export cleaned CSV and Excel files
- 🎨 Professional Streamlit dashboard

## 🛠️ Tech Stack

- Python
- Pandas
- NumPy
- Streamlit
- OpenAI-compatible API
- Google Gemini
- Pytest
- Excel / CSV

## 🏗️ Project Structure

```text
AI-data-cleaning-assistant/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── src/
│   ├── __init__.py
│   ├── data_loader.py
│   ├── profiler.py
│   ├── anomaly_detector.py
│   ├── cleaner.py
│   └── ai_assistant.py
│
└── test/
    ├── test_loader.py
    ├── test_cleaner.py
    └── test_ai_assistant.py
