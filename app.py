import io

import pandas as pd
import streamlit as st

from src.profiler import profile_dataset
from src.anomaly_detector import detect_all_anomalies
from src.ai_assistant import generate_ai_recommendations
from src.cleaner import clean_dataset


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AI Data Cleaning Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# SESSION STATE
# ============================================================

defaults = {
    "df": None,
    "profile": None,
    "issues": None,
    "ai_result": None,
    "cleaned_df": None,
    "audit_log": None,
    "file_name": None
}

for key, value in defaults.items():

    if key not in st.session_state:
        st.session_state[key] = value


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def load_dataset(uploaded_file):
    """
    Load CSV or Excel dataset.
    """

    filename = uploaded_file.name.lower()

    if filename.endswith(".csv"):

        return pd.read_csv(
            uploaded_file
        )

    if filename.endswith(".xlsx"):

        return pd.read_excel(
            uploaded_file
        )

    if filename.endswith(".xls"):

        return pd.read_excel(
            uploaded_file
        )

    raise ValueError(
        "Unsupported file format."
    )


def calculate_quality_score(df):
    """
    Calculate a simple data-quality score.

    This score considers:
    - Missing values
    - Duplicate rows
    """

    if df is None or df.empty:
        return 0.0

    total_cells = (
        df.shape[0] *
        df.shape[1]
    )

    if total_cells == 0:
        return 0.0

    missing_values = int(
        df.isna().sum().sum()
    )

    duplicate_rows = int(
        df.duplicated().sum()
    )

    missing_rate = (
        missing_values /
        total_cells
    )

    duplicate_rate = (
        duplicate_rows /
        len(df)
    )

    score = 100

    score -= (
        missing_rate * 60
    )

    score -= (
        duplicate_rate * 30
    )

    return round(
        max(
            0,
            min(
                score,
                100
            )
        ),
        1
    )


def calculate_issue_counts(issues):
    """
    Count detected issues by type.
    """

    counts = {}

    for issue in issues:

        issue_type = issue.get(
            "type",
            "unknown"
        )

        counts[issue_type] = (
            counts.get(
                issue_type,
                0
            ) + 1
        )

    return counts


def calculate_severity_counts(issues):
    """
    Count issues by severity.
    """

    severity_counts = {
        "high": 0,
        "medium": 0,
        "low": 0
    }

    for issue in issues:

        severity = str(
            issue.get(
                "severity",
                ""
            )
        ).lower()

        if severity in severity_counts:

            severity_counts[
                severity
            ] += 1

    return severity_counts


def dataframe_to_excel(df):
    """
    Convert DataFrame to Excel bytes.
    """

    output = io.BytesIO()

    with pd.ExcelWriter(
        output,
        engine="openpyxl"
    ) as writer:

        df.to_excel(
            writer,
            index=False,
            sheet_name="Cleaned Data"
        )

    return output.getvalue()


# ============================================================
# HEADER
# ============================================================

st.title("🤖 AI Data Cleaning Assistant")

st.caption(
    "Automated Data Quality Analysis, "
    "AI Recommendations & Intelligent Cleaning"
)

# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header(
        "📁 Dataset"
    )

    uploaded_file = st.file_uploader(
        "Upload CSV or Excel",
        type=[
            "csv",
            "xlsx",
            "xls"
        ]
    )

    st.divider()

    st.markdown(
        """
        ### 🔄 Processing Pipeline

        📥 Upload Dataset

        ↓

        📊 Profile Dataset

        ↓

        🚨 Detect Issues

        ↓

        🤖 AI Recommendations

        ↓

        🧹 Clean Dataset

        ↓

        📤 Export Results
        """
    )

    st.divider()

    st.caption(
        "AI Data Cleaning Assistant v1.0"
    )


# ============================================================
# NO DATASET
# ============================================================

if uploaded_file is None:

    st.info(
        "👈 Upload a CSV or Excel dataset "
        "from the sidebar to begin."
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.markdown(
            "### 📊 Profile"
        )

        st.write(
            "Analyze rows, columns, "
            "data types and missing values."
        )

    with col2:

        st.markdown(
            "### 🚨 Detect"
        )

        st.write(
            "Detect missing values, "
            "duplicates, outliers and "
            "category inconsistencies."
        )

    with col3:

        st.markdown(
            "### 🤖 Recommend"
        )

        st.write(
            "Use Gemini to generate "
            "practical data-cleaning "
            "recommendations."
        )

    st.stop()


# ============================================================
# LOAD DATASET
# ============================================================

if (
    st.session_state.file_name
    != uploaded_file.name
):

    try:

        df = load_dataset(
            uploaded_file
        )

        st.session_state.df = df

        st.session_state.file_name = (
            uploaded_file.name
        )

        # Reset previous analysis

        st.session_state.profile = None

        st.session_state.issues = None

        st.session_state.ai_result = None

        st.session_state.cleaned_df = None

        st.session_state.audit_log = None

    except Exception as e:

        st.error(
            "❌ Failed to load dataset."
        )

        st.exception(e)

        st.stop()

else:

    df = st.session_state.df


# ============================================================
# VALIDATE DATASET
# ============================================================

if df is None:

    st.error(
        "Dataset could not be loaded."
    )

    st.stop()


if df.empty:

    st.warning(
        "The uploaded dataset contains no rows."
    )

    st.stop()


# ============================================================
# LOCAL DATA ANALYSIS
# ============================================================

if st.session_state.profile is None:

    with st.spinner(
        "📊 Profiling dataset..."
    ):

        try:

            st.session_state.profile = (
                profile_dataset(df)
            )

        except Exception as e:

            st.error(
                "❌ Dataset profiling failed."
            )

            st.exception(e)

            st.stop()


if st.session_state.issues is None:

    with st.spinner(
        "🔍 Detecting data-quality issues..."
    ):

        try:

            st.session_state.issues = (
                detect_all_anomalies(df)
            )

        except Exception as e:

            st.error(
                "❌ Issue detection failed."
            )

            st.exception(e)

            st.stop()


profile = st.session_state.profile

issues = st.session_state.issues


# ============================================================
# CALCULATE DASHBOARD METRICS
# ============================================================

rows = len(df)

columns = len(df.columns)

missing_values = int(
    df.isna().sum().sum()
)

duplicates = int(
    df.duplicated().sum()
)

quality_score = (
    calculate_quality_score(df)
)

issue_counts = (
    calculate_issue_counts(
        issues
    )
)

severity_counts = (
    calculate_severity_counts(
        issues
    )
)


# ============================================================
# DATASET STATUS
# ============================================================

st.success(
    f"✅ Dataset loaded successfully: "
    f"**{uploaded_file.name}**"
)


# ============================================================
# KPI CARDS
# ============================================================

col1, col2, col3, col4, col5 = st.columns(5)


with col1:

    st.metric(
        "📄 Records",
        f"{rows:,}"
    )


with col2:

    st.metric(
        "📊 Features",
        columns
    )


with col3:

    st.metric(
        "🚨 Issues",
        len(issues)
    )


with col4:

    st.metric(
        "❗ Missing",
        missing_values
    )


with col5:

    st.metric(
        "🎯 Quality",
        f"{quality_score}%"
    )


# ============================================================
# QUALITY STATUS
# ============================================================

st.divider()


if quality_score >= 90:

    st.success(
        "🟢 **Excellent Data Quality** — "
        "Dataset is ready for downstream analysis."
    )

elif quality_score >= 75:

    st.warning(
        "🟡 **Moderate Data Quality** — "
        "Some cleaning is recommended."
    )

else:

    st.error(
        "🔴 **Poor Data Quality** — "
        "Cleaning is strongly recommended."
    )


# ============================================================
# MAIN TABS
# ============================================================

tab_dashboard, tab_quality, tab_ai, tab_clean, tab_export = (
    st.tabs(
        [
            "📊 Dashboard",
            "🔍 Data Quality",
            "🤖 AI Recommendations",
            "🧹 Cleaning",
            "📥 Export"
        ]
    )
)


# ============================================================
# DASHBOARD TAB
# ============================================================

with tab_dashboard:

    st.header(
        "📊 Data Quality Dashboard"
    )

    # --------------------------------------------------------
    # QUALITY SCORE
    # --------------------------------------------------------

    st.subheader(
        "🎯 Overall Data Quality"
    )

    score_col1, score_col2 = st.columns(
        [1, 3]
    )

    with score_col1:

        st.metric(
            "Quality Score",
            f"{quality_score}%"
        )

    with score_col2:

        st.progress(
            quality_score / 100
        )

    st.divider()

    # --------------------------------------------------------
    # ISSUE BREAKDOWN
    # --------------------------------------------------------

    st.subheader(
        "🚨 Issue Breakdown"
    )

    if issue_counts:

        issue_df = pd.DataFrame(
            {
                "Issue Type": list(
                    issue_counts.keys()
                ),
                "Count": list(
                    issue_counts.values()
                )
            }
        )

        issue_df = issue_df.sort_values(
            "Count",
            ascending=True
        )

        st.bar_chart(
            issue_df.set_index(
                "Issue Type"
            ),
            horizontal=True
        )

    else:

        st.success(
            "🎉 No data-quality issues detected."
        )

    st.divider()

    # --------------------------------------------------------
    # SEVERITY
    # --------------------------------------------------------

    st.subheader(
        "🚦 Issue Severity"
    )

    s1, s2, s3 = st.columns(3)

    with s1:

        st.metric(
            "🔴 High",
            severity_counts["high"]
        )

    with s2:

        st.metric(
            "🟡 Medium",
            severity_counts["medium"]
        )

    with s3:

        st.metric(
            "🟢 Low",
            severity_counts["low"]
        )

    st.divider()

    # --------------------------------------------------------
    # DATA HEALTH
    # --------------------------------------------------------

    st.subheader(
        "❤️ Data Health"
    )

    h1, h2, h3 = st.columns(3)

    with h1:

        st.metric(
            "Missing Values",
            missing_values
        )

    with h2:

        st.metric(
            "Duplicate Rows",
            duplicates
        )

    with h3:

        st.metric(
            "Outlier Issues",
            issue_counts.get(
                "outliers",
                0
            )
        )

    st.divider()

    # --------------------------------------------------------
    # DATA PREVIEW
    # --------------------------------------------------------

    st.subheader(
        "👀 Dataset Preview"
    )

    st.dataframe(
        df.head(100),
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# DATA QUALITY TAB
# ============================================================

with tab_quality:

    st.header(
        "🔍 Detected Data-Quality Issues"
    )

    if not issues:

        st.success(
            "🎉 No data-quality issues detected."
        )

    else:

        st.warning(
            f"⚠️ {len(issues)} issue(s) "
            "detected by the Python engine."
        )

        issue_df = pd.DataFrame(
            issues
        )

        st.dataframe(
            issue_df,
            use_container_width=True,
            hide_index=True
        )

        st.divider()

        st.subheader(
            "Issue Details"
        )

        for index, issue in enumerate(
            issues,
            start=1
        ):

            issue_type = issue.get(
                "type",
                "Unknown"
            )

            severity = str(
                issue.get(
                    "severity",
                    "Unknown"
                )
            ).lower()

            if severity == "high":

                icon = "🔴"

            elif severity == "medium":

                icon = "🟡"

            else:

                icon = "🟢"

            with st.expander(
                f"{icon} {index}. "
                f"{issue_type} "
                f"— {severity.upper()}"
            ):

                for key, value in issue.items():

                    st.write(
                        f"**{key}:** {value}"
                    )


# ============================================================
# AI RECOMMENDATIONS TAB
# ============================================================

with tab_ai:

    st.header(
        "🤖 Gemini AI Recommendations"
    )

    st.write(
        """
        The Python data-quality engine performs the actual
        dataset analysis. Gemini receives only the detected
        issues and provides concise recommendations.
        """
    )

    if not issues:

        st.success(
            "🎉 No issues detected. "
            "AI analysis is not required."
        )

    else:

        st.info(
            f"🤖 Gemini will provide recommendations "
            f"for **{len(issues)} issues** detected by "
            "the Python data-quality engine."
        )

        if st.button(
            "🚀 Generate AI Recommendations",
            type="primary"
        ):

            with st.spinner(
                "🤖 Gemini is generating recommendations..."
            ):

                try:

                    result = (
                        generate_ai_recommendations(
                            issues
                        )
                    )

                    st.session_state.ai_result = (
                        result
                    )

                except Exception as e:

                    st.error(
                        "❌ Gemini request failed."
                    )

                    st.exception(e)

    # --------------------------------------------------------
    # DISPLAY AI RESULT
    # --------------------------------------------------------

    if st.session_state.ai_result:

        result = (
            st.session_state.ai_result
        )

        if "error" in result:

            st.error(
                result.get(
                    "summary",
                    "AI analysis failed."
                )
            )

            st.code(
                str(
                    result["error"]
                )
            )

        else:

            st.success(
                "✅ AI analysis completed."
            )

            st.subheader(
                "🧠 Executive Summary"
            )

            st.info(
                result.get(
                    "summary",
                    "No summary available."
                )
            )

            recommendations = (
                result.get(
                    "recommendations",
                    []
                )
            )

            st.subheader(
                "💡 Recommendations"
            )

            if not recommendations:

                st.info(
                    "No recommendations returned."
                )

            for index, rec in enumerate(
                recommendations,
                start=1
            ):

                issue_type = rec.get(
                    "issue_type",
                    "Unknown"
                )

                severity = str(
                    rec.get(
                        "severity",
                        "N/A"
                    )
                ).lower()

                if severity == "high":

                    icon = "🔴"

                elif severity == "medium":

                    icon = "🟡"

                else:

                    icon = "🟢"

                with st.container(
                    border=True
                ):

                    st.markdown(
                        f"### {icon} {index}. "
                        f"{issue_type}"
                    )

                    c1, c2 = st.columns(
                        [3, 1]
                    )

                    with c1:

                        st.write(
                            "**Column:**",
                            rec.get(
                                "column",
                                "N/A"
                            )
                        )

                        st.write(
                            "**Recommended Action:**",
                            rec.get(
                                "recommended_action",
                                "N/A"
                            )
                        )

                        st.write(
                            "**Reason:**",
                            rec.get(
                                "reason",
                                "N/A"
                            )
                        )

                    with c2:

                        confidence = rec.get(
                            "confidence",
                            None
                        )

                        if confidence is not None:

                            try:

                                confidence = float(
                                    confidence
                                )

                                if confidence <= 1:

                                    confidence *= 100

                                st.metric(
                                    "Confidence",
                                    f"{confidence:.0f}%"
                                )

                            except (
                                ValueError,
                                TypeError
                            ):

                                st.metric(
                                    "Confidence",
                                    "N/A"
                                )

                        st.metric(
                            "Severity",
                            severity.upper()
                        )


# ============================================================
# CLEANING TAB
# ============================================================

with tab_clean:

    st.header(
        "🧹 Dataset Cleaning"
    )

    st.write(
        """
        Run the automated Python cleaning pipeline.
        All cleaning actions are recorded in the audit log.
        """
    )

    if st.button(
        "🧹 Run Cleaning Pipeline",
        type="primary"
    ):

        with st.spinner(
            "🧹 Cleaning dataset..."
        ):

            try:

                cleaned_df, audit_log = (
                    clean_dataset(df)
                )

                st.session_state.cleaned_df = (
                    cleaned_df
                )

                st.session_state.audit_log = (
                    audit_log
                )

                st.success(
                    "✅ Dataset cleaned successfully!"
                )

            except Exception as e:

                st.error(
                    "❌ Cleaning failed."
                )

                st.exception(e)

    # --------------------------------------------------------
    # BEFORE / AFTER
    # --------------------------------------------------------

    if st.session_state.cleaned_df is not None:

        cleaned_df = (
            st.session_state.cleaned_df
        )

        audit_log = (
            st.session_state.audit_log
        )

        st.divider()

        st.subheader(
            "📈 Cleaning Impact"
        )

        before_score = (
            calculate_quality_score(
                df
            )
        )

        after_score = (
            calculate_quality_score(
                cleaned_df
            )
        )

        score_improvement = (
            after_score -
            before_score
        )

        before_missing = int(
            df.isna().sum().sum()
        )

        after_missing = int(
            cleaned_df.isna().sum().sum()
        )

        before_duplicates = int(
            df.duplicated().sum()
        )

        after_duplicates = int(
            cleaned_df.duplicated().sum()
        )

        # ----------------------------------------------------
        # BEFORE
        # ----------------------------------------------------

        before_col, after_col = st.columns(2)

        with before_col:

            st.markdown(
                "### 🔴 Before Cleaning"
            )

            st.metric(
                "Quality Score",
                f"{before_score}%"
            )

            st.metric(
                "Missing Values",
                before_missing
            )

            st.metric(
                "Duplicate Rows",
                before_duplicates
            )

        # ----------------------------------------------------
        # AFTER
        # ----------------------------------------------------

        with after_col:

            st.markdown(
                "### 🟢 After Cleaning"
            )

            st.metric(
                "Quality Score",
                f"{after_score}%"
            )

            st.metric(
                "Missing Values",
                after_missing
            )

            st.metric(
                "Duplicate Rows",
                after_duplicates
            )

        # ----------------------------------------------------
        # IMPROVEMENT
        # ----------------------------------------------------

        st.divider()

        if score_improvement > 0:

            st.success(
                f"📈 Quality score improved by "
                f"**{score_improvement:.1f} points**."
            )

        elif score_improvement == 0:

            st.info(
                "Quality score remained unchanged."
            )

        else:

            st.warning(
                "Quality score decreased after cleaning. "
                "Review the audit log."
            )

        # ----------------------------------------------------
        # CLEANED DATA PREVIEW
        # ----------------------------------------------------

        st.divider()

        st.subheader(
            "👀 Cleaned Dataset Preview"
        )

        st.dataframe(
            cleaned_df.head(100),
            use_container_width=True,
            hide_index=True
        )

        # ----------------------------------------------------
        # AUDIT LOG
        # ----------------------------------------------------

        st.divider()

        st.subheader(
            "📜 Cleaning Audit Log"
        )

        if audit_log:

            audit_df = pd.DataFrame(
                audit_log
            )

            st.dataframe(
                audit_df,
                use_container_width=True,
                hide_index=True
            )

        else:

            st.info(
                "No cleaning actions were required."
            )


# ============================================================
# EXPORT TAB
# ============================================================

with tab_export:

    st.header(
        "📥 Export Results"
    )

    if st.session_state.cleaned_df is None:

        st.info(
            "🧹 Run the cleaning pipeline first "
            "to enable exports."
        )

    else:

        cleaned_df = (
            st.session_state.cleaned_df
        )

        audit_log = (
            st.session_state.audit_log
        )

        # ----------------------------------------------------
        # CSV
        # ----------------------------------------------------

        st.subheader(
            "📄 Clean CSV"
        )

        csv_data = (
            cleaned_df
            .to_csv(
                index=False
            )
            .encode("utf-8")
        )

        st.download_button(
            "⬇️ Download Clean CSV",
            data=csv_data,
            file_name="cleaned_dataset.csv",
            mime="text/csv"
        )

        # ----------------------------------------------------
        # EXCEL
        # ----------------------------------------------------

        st.subheader(
            "📊 Clean Excel"
        )

        try:

            excel_data = (
                dataframe_to_excel(
                    cleaned_df
                )
            )

            st.download_button(
                "⬇️ Download Clean Excel",
                data=excel_data,
                file_name="cleaned_dataset.xlsx",
                mime=(
                    "application/"
                    "vnd.openxmlformats-officedocument."
                    "spreadsheetml.sheet"
                )
            )

        except Exception as e:

            st.error(
                "❌ Excel generation failed."
            )

            st.exception(e)

        # ----------------------------------------------------
        # AUDIT LOG
        # ----------------------------------------------------

        if audit_log:

            st.subheader(
                "📜 Cleaning Audit Log"
            )

            audit_data = (
                pd.DataFrame(
                    audit_log
                )
                .to_csv(
                    index=False
                )
                .encode("utf-8")
            )

            st.download_button(
                "⬇️ Download Audit Log",
                data=audit_data,
                file_name="cleaning_audit_log.csv",
                mime="text/csv"
            )

        st.success(
            "✅ Export files are ready."
        )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "AI Data Cleaning Assistant • "
    "Python + Pandas + Streamlit + Gemini"
)