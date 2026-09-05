# 🤖 AI Data Cleaning Assistant

An AI-powered **data quality and data cleaning application** built with Python and Streamlit.

The application allows users to upload CSV or Excel datasets, automatically profile the data, identify data-quality issues and statistical anomalies, receive AI-powered recommendations using **Google Gemini**, clean the dataset, compare data quality before and after cleaning, and export the cleaned dataset along with an audit log.

🌐 **Live Demo:** [https://ai-data-cleaning-assistant.streamlit.app/](https://ai-data-cleaning-assistant-hpfcysucdn8zgs7mtpqdf8.streamlit.app/)

📂 **GitHub Repository:**  
https://github.com/Jaiswalaniket989/AI-data-cleaning-assistant

---

## 📌 Project Overview

Data cleaning and data-quality analysis are often repetitive and time-consuming parts of the data-analysis workflow.

This project automates common data-quality tasks through an interactive Streamlit application.

The system combines traditional Python-based data processing with Generative AI to provide an end-to-end workflow:

```text
Upload → Profile → Detect → Analyze → Recommend → Clean → Validate → Export
```

The application is designed so that **deterministic Python logic handles data detection and cleaning**, while **Google Gemini provides recommendations and explanations** based on the detected issues.

---

# 🚀 Features

## 📂 Data Upload

- Upload CSV files
- Upload Excel files (`.xlsx`, `.xls`)
- Automatic dataset loading
- Preview uploaded data

---

## 🔍 Automated Data Profiling

The application analyzes the uploaded dataset and provides information such as:

- Number of records
- Number of columns
- Data types
- Missing values
- Duplicate records
- Unique values
- Basic dataset statistics
- Overall data-quality information

---

## ⚠️ Data Quality Issue Detection

The system identifies common data-quality problems, including:

- Missing values
- Duplicate records
- Inconsistent categorical values
- Invalid numeric values
- Statistical outliers
- Potential anomalies

Issues are categorized and presented through the dashboard for easier interpretation.

---

## 🚨 Statistical Anomaly Detection

Numeric columns are analyzed using statistical techniques to identify unusually high or low observations.

The anomaly detection component evaluates numeric values and identifies observations that deviate significantly from the normal distribution of the data.

Detected anomalies can include:

- Metric/column name
- Observed value
- Mean value
- Direction of deviation
- Deviation percentage
- Z-score
- Severity

---

## 🤖 AI-Powered Recommendations

Google Gemini is integrated into the application using an OpenAI-compatible API interface.

The AI layer receives **only the detected data-quality issues**, rather than the complete dataset.

Gemini generates:

- Overall data-quality summary
- Recommended action
- Reason for recommendation
- Issue severity
- Confidence score

The AI is used as a **recommendation layer**, while the core issue detection remains deterministic and programmatic.

This helps make the application:

- Faster
- More predictable
- Easier to test
- More focused
- Less dependent on AI for data detection

---

## 🧹 Automated Data Cleaning

The cleaning pipeline can automatically perform several data-cleaning operations.

### Duplicate Removal

Removes duplicate records from the dataset.

### Numeric Missing-Value Imputation

Missing numeric values are filled using the **median** of the corresponding column.

### Categorical Missing-Value Imputation

Missing categorical values are filled using the **mode** of the corresponding column.

### Category Standardization

Categorical values are standardized to reduce inconsistent representations.

### Numeric Conversion

Applicable columns are converted into appropriate numeric formats.

### Outlier Handling

Extreme numeric observations are handled using the **Interquartile Range (IQR)** method.

---

## 📊 Before vs After Data Quality

The application compares dataset quality before and after cleaning.

The comparison can include:

- Missing values
- Duplicate records
- Number of detected issues
- Data-quality score
- Improvement after cleaning

This provides users with measurable evidence of the cleaning process.

---

## 📝 Cleaning Audit Log

Every cleaning operation can be recorded in an audit log.

The audit information can be used to understand:

- What cleaning operation was performed
- Which issue was addressed
- What changed in the dataset
- The overall cleaning process

The audit log can also be exported for documentation.

---

## 📥 Export

Users can export the processed results in multiple formats.

Supported outputs include:

- Cleaned CSV
- Cleaned Excel workbook
- Cleaning audit log

---

## 🎨 Professional Streamlit Dashboard

The project includes an interactive dashboard built with Streamlit.

Main sections include:

- Dashboard
- Data Quality
- AI Recommendations
- Cleaning
- Export

The interface provides an end-to-end workflow without requiring users to write Python code.

---

# 🏗️ System Architecture

```text
                         ┌──────────────────────┐
                         │       User           │
                         │   CSV / Excel File   │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │     Data Loader      │
                         │    data_loader.py    │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │    Data Profiler     │
                         │      profiler.py     │
                         └──────────┬───────────┘
                                    │
                                    ▼
                    ┌───────────────────────────────┐
                    │     Data Quality Detection    │
                    └──────────────┬────────────────┘
                                   │
                    ┌──────────────┴───────────────┐
                    │                              │
                    ▼                              ▼
          ┌───────────────────┐          ┌───────────────────┐
          │ Anomaly Detector  │          │  Issue Analysis   │
          │ anomaly_detector  │          │ Missing / Dupes   │
          └─────────┬─────────┘          └─────────┬─────────┘
                    │                              │
                    └──────────────┬───────────────┘
                                   │
                                   ▼
                         ┌──────────────────────┐
                         │    AI Assistant      │
                         │   ai_assistant.py    │
                         │      Gemini API      │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │   Cleaning Pipeline  │
                         │      cleaner.py      │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │ Before / After Check │
                         │   Quality Comparison  │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │   Export Clean Data  │
                         │ + Audit Log / Excel  │
                         └──────────────────────┘
```

---

# 🔄 Application Workflow

```text
1. Upload CSV / Excel Dataset
              ↓
2. Load Dataset
              ↓
3. Profile Dataset
              ↓
4. Detect Data Quality Issues
              ↓
5. Detect Statistical Anomalies
              ↓
6. Generate AI Recommendations
              ↓
7. Run Cleaning Pipeline
              ↓
8. Compare Before vs After Quality
              ↓
9. Generate Audit Log
              ↓
10. Export Clean Dataset
```

---

# 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core application logic |
| Pandas | Data processing and transformation |
| NumPy | Numerical analysis |
| Streamlit | Interactive web application |
| Google Gemini | AI-powered recommendations |
| OpenAI Python SDK | Gemini API integration |
| python-dotenv | Local environment variable management |
| Pytest | Automated testing |
| Git | Version control |
| GitHub | Source-code hosting |
| Streamlit Community Cloud | Application deployment |
| CSV / Excel | Input and output formats |

---

# 📁 Project Structure

```text
AI-data-cleaning-assistant/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── data/
│   └── input/
│       └── sample_sales.csv
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
    ├── __init__.py
    ├── run_ai.py
    ├── test_ai_assistant.py
    ├── test_anomaly_detector.py
    ├── test_cleaner.py
    ├── test_cleaning_output.py
    ├── test_loader.py
    └── test_profiler.py
```

---

# ⚙️ Installation

## 1. Clone the repository

```bash
git clone https://github.com/Jaiswalaniket989/AI-data-cleaning-assistant.git
```

## 2. Navigate into the project

```bash
cd AI-data-cleaning-assistant
```

## 3. Create a virtual environment

```bash
python -m venv .venv
```

## 4. Activate the virtual environment

### Windows PowerShell

```powershell
.\.venv\Scripts\Activate.ps1
```

### Windows Command Prompt

```cmd
.venv\Scripts\activate
```

## 5. Install dependencies

```bash
pip install -r requirements.txt
```

---

# 🔐 Environment Variables

For local development, create a `.env` file in the project root.

```env
GEMINI_API_KEY=your_gemini_api_key
```

The `.env` file must remain private and should **never be committed to GitHub**.

The repository `.gitignore` is configured to exclude it.

---

# ▶️ Run the Application

Start the Streamlit application using:

```bash
python -m streamlit run app.py
```

The application will open in your browser.

---

# 🧪 Testing

The project uses **Pytest** for automated testing.

Run the complete test suite:

```bash
python -m pytest
```

The project currently includes tests covering:

- Data loading
- Data profiling
- Data cleaning
- Anomaly detection
- AI assistant functionality

Example test files:

```text
test/test_loader.py
test/test_profiler.py
test/test_cleaner.py
test/test_anomaly_detector.py
test/test_ai_assistant.py
```

---

# 🤖 AI Integration Design

The AI component is intentionally separated from the core data-processing pipeline.

```text
Dataset
   ↓
Python Detection
   ↓
Detected Issues
   ↓
Gemini
   ↓
Recommendations
```

Gemini does **not** perform the entire data-quality analysis from scratch.

Instead:

1. Python analyzes the dataset.
2. Data-quality issues are detected programmatically.
3. Only relevant issue information is sent to Gemini.
4. Gemini explains the issues and recommends practical actions.
5. The application displays the recommendations.

This design provides a clear separation between:

```text
Deterministic Data Processing
              +
Generative AI Recommendations
```

---

# 🧹 Cleaning Strategy

The automated cleaning pipeline includes the following operations:

```text
Duplicate Removal
        ↓
Numeric Missing Values
        ↓
Categorical Missing Values
        ↓
Category Standardization
        ↓
Numeric Conversion
        ↓
IQR Outlier Capping
```

### Numeric Imputation

Median imputation is used because it is less sensitive to extreme values than mean imputation.

### Categorical Imputation

Mode imputation is used for categorical columns with missing values.

### Outlier Handling

The Interquartile Range method is used to identify extreme observations.

```text
IQR = Q3 - Q1

Lower Bound = Q1 - 1.5 × IQR
Upper Bound = Q3 + 1.5 × IQR
```

Values outside the expected range can be capped rather than removed.

---

# 📊 Data Quality Scoring

The dashboard provides an overall data-quality score based on detected issues.

The score can help users quickly understand whether the dataset is:

- Healthy
- Needs attention
- Requires significant cleaning

The score is recalculated after cleaning to demonstrate improvement.

---

# ☁️ Deployment

The application is deployed using **Streamlit Community Cloud**.

The deployment process uses:

```text
GitHub Repository
        ↓
Streamlit Community Cloud
        ↓
app.py
        ↓
Streamlit Application
```

For cloud deployment, the Gemini API key is stored securely using **Streamlit Secrets**.

Example TOML configuration:

```toml
GEMINI_API_KEY = "your_gemini_api_key"
```

The API key is not stored in the GitHub repository.

---

# 🔒 Security

Sensitive configuration is intentionally separated from source code.

Local development:

```text
.env
   ↓
GEMINI_API_KEY
```

Cloud deployment:

```text
Streamlit Secrets
   ↓
GEMINI_API_KEY
```

The `.gitignore` file excludes:

```text
.env
.venv/
__pycache__/
*.pyc
.pytest_cache/
.streamlit/secrets.toml
```

---

# 📸 Screenshots

Add screenshots of the deployed application here.

Recommended screenshots:

### Dashboard

```text
screenshots/dashboard.png
```

### Data Quality

```text
screenshots/data-quality.png
```

### AI Recommendations

```text
screenshots/ai-recommendations.png
```

### Cleaning Results

```text
screenshots/cleaning-results.png
```

### Export

```text
screenshots/export.png
```

Once the images are added to the repository, they can be displayed using:

```markdown
![Dashboard](screenshots/dashboard.png)

![Data Quality](screenshots/data-quality.png)

![AI Recommendations](screenshots/ai-recommendations.png)

![Cleaning Results](screenshots/cleaning-results.png)
```

---

# 📈 Project Results

The project demonstrates an end-to-end automated data-quality workflow capable of:

- Reading real-world tabular datasets
- Identifying common data-quality problems
- Detecting statistical anomalies
- Generating AI-powered recommendations
- Applying automated cleaning operations
- Measuring quality improvement
- Recording cleaning actions
- Exporting cleaned datasets

The application combines **Data Engineering + Data Analytics + Generative AI + Software Testing + Cloud Deployment** into a single portfolio project.

---

# 🎯 Project Objectives

The main objectives of this project are to demonstrate practical experience in:

- Python programming
- Pandas
- NumPy
- Data cleaning
- Data-quality analysis
- Statistical anomaly detection
- Generative AI integration
- API integration
- Streamlit application development
- Automated testing
- Git/GitHub
- Cloud deployment

---

# 💡 Why This Project?

A typical data-analysis workflow may require analysts to repeatedly:

```text
Open Dataset
    ↓
Check Missing Values
    ↓
Find Duplicates
    ↓
Check Data Types
    ↓
Search for Outliers
    ↓
Clean the Data
    ↓
Validate Again
```

This project automates much of that workflow through a single application.

Instead of manually performing repetitive checks, users can upload their dataset and receive a structured overview of its quality.

---

# 🔮 Future Improvements

Potential future enhancements include:

- Automated PDF data-quality reports
- Advanced anomaly detection models
- Machine-learning-based anomaly detection
- Interactive data visualizations
- Custom data-cleaning rules
- Database connectivity
- SQL data-source support
- Scheduled data-quality monitoring
- Automated email reports
- User authentication
- Role-based access
- Larger dataset optimization
- Multiple AI-provider support
- Data-quality rule configuration
- Data lineage tracking

---

# 🧪 Example Use Cases

This application can be useful for:

### Data Analysts

Quickly profile and clean datasets before analysis.

### Business Analysts

Identify data-quality issues before preparing reports.

### MIS Teams

Automate repetitive spreadsheet-cleaning tasks.

### Data Engineers

Prototype data-quality checks before integrating them into larger pipelines.

### Students / Learners

Understand practical implementation of data cleaning, anomaly detection, AI integration, testing, and deployment.

---

# 📚 Learning Outcomes

Through this project, the following concepts were applied:

```text
Python
   ↓
Pandas / NumPy
   ↓
Data Cleaning
   ↓
Data Profiling
   ↓
Statistical Analysis
   ↓
Anomaly Detection
   ↓
Generative AI
   ↓
API Integration
   ↓
Streamlit
   ↓
Testing
   ↓
Git/GitHub
   ↓
Cloud Deployment
```

---

# 👨‍💻 Author

## Aniket Jaiswal

**Data Analyst | Python | SQL | Power BI | Excel**

### LinkedIn

https://www.linkedin.com/in/aniket-jaiswal-27b224275/

### GitHub

https://github.com/Jaiswalaniket989

### Project Repository

https://github.com/Jaiswalaniket989/AI-data-cleaning-assistant

---

# ⭐ Project Highlights

This project demonstrates an end-to-end practical data workflow:

```text
INGEST
   ↓
PROFILE
   ↓
DETECT
   ↓
ANALYZE
   ↓
RECOMMEND
   ↓
CLEAN
   ↓
VALIDATE
   ↓
EXPORT
```

### Core Strengths

✅ Automated data-quality analysis  
✅ Statistical anomaly detection  
✅ AI-powered recommendations  
✅ Automated data cleaning  
✅ Before/after validation  
✅ Audit logging  
✅ CSV and Excel support  
✅ Pytest test coverage  
✅ Git/GitHub workflow  
✅ Streamlit Cloud deployment  

---

## 🌟 Final Summary

**AI Data Cleaning Assistant** is a practical end-to-end data-quality automation project that combines traditional data-processing techniques with Generative AI.

It demonstrates how Python, Pandas, statistical analysis, Gemini, Streamlit, automated testing, GitHub, and cloud deployment can be combined to build a real-world data application.
