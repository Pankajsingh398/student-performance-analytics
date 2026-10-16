import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

st.set_page_config(page_title="Student Performance Analytics", page_icon="📊", layout="wide")

st.title("📊 Student Performance Analytics & Prediction System")
st.caption("A Python data analytics project using Pandas, Matplotlib and Streamlit")

REQUIRED = ["student_id", "name", "attendance", "study_hours", "marks"]

@st.cache_data
def load_sample():
    path = Path(__file__).parent / "students.csv"
    return pd.read_csv(path)

def prepare_data(df):
    df = df.copy()
    df.columns = [str(c).strip().lower().replace(" ", "_") for c in df.columns]
    missing = [c for c in REQUIRED if c not in df.columns]
    if missing:
        raise ValueError("Missing required columns: " + ", ".join(missing))
    for col in ["attendance", "study_hours", "marks"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df = df.dropna(subset=["attendance", "study_hours", "marks"])
    df["attendance"] = df["attendance"].clip(0, 100)
    df["marks"] = df["marks"].clip(0, 100)
    df["study_hours"] = df["study_hours"].clip(lower=0)
    df["performance"] = np.where(df["marks"] >= 40, "Pass", "Needs Improvement")
    df["risk_level"] = np.select(
        [
            (df["attendance"] < 65) | (df["marks"] < 35),
            (df["attendance"] < 75) | (df["marks"] < 50),
        ],
        ["High", "Medium"],
        default="Low"
    )
    return df

with st.sidebar:
    st.header("📂 Data")
    uploaded = st.file_uploader("Upload a CSV file", type=["csv"])
    st.markdown("**Required columns:**")
    st.code("student_id, name, attendance, study_hours, marks", language="text")
    st.caption("No file? The app uses the included sample dataset.")
    st.divider()
    st.markdown("**Filters**")

try:
    raw = pd.read_csv(uploaded) if uploaded is not None else load_sample()
    df = prepare_data(raw)
except Exception as e:
    st.error(f"Could not load the dataset: {e}")
    st.info("Check that your CSV includes all five required columns.")
    st.stop()

if df.empty:
    st.warning("No usable records found. Check that attendance, study_hours and marks contain numbers.")
    st.stop()

with st.sidebar:
    min_marks = st.slider("Minimum marks", 0, 100, 0)
    max_marks = st.slider("Maximum marks", 0, 100, 100)
    selected_risk = st.multiselect("Risk level", ["High", "Medium", "Low"], default=["High", "Medium", "Low"])

filtered = df[
    df["marks"].between(min_marks, max_marks) &
    df["risk_level"].isin(selected_risk)
]

if filtered.empty:
    st.warning("No students match these filters. Change the filters in the sidebar.")
    st.stop()

c1, c2, c3, c4 = st.columns(4)
c1.metric("Total students", f"{len(filtered)}")
c2.metric("Average marks", f"{filtered['marks'].mean():.1f}/100")
c3.metric("Pass percentage", f"{(filtered['marks'].ge(40).mean() * 100):.1f}%")
c4.metric("High-risk students", f"{(filtered['risk_level'].eq('High').sum())}")

tab1, tab2, tab3 = st.tabs(["📈 Dashboard", "🧑‍🎓 Student Records", "💡 Insights & Prediction"])

with tab1:
    left, right = st.columns(2)
    with left:
        st.subheader("Marks distribution")
        fig, ax = plt.subplots()
        ax.hist(filtered["marks"], bins=10, edgecolor="black")
        ax.set_xlabel("Marks")
        ax.set_ylabel("Number of students")
        ax.set_title("Distribution of student marks")
        st.pyplot(fig)
        plt.close(fig)
    with right:
        st.subheader("Attendance vs Marks")
        fig, ax = plt.subplots()
        ax.scatter(filtered["attendance"], filtered["marks"])
        ax.set_xlabel("Attendance (%)")
        ax.set_ylabel("Marks")
        ax.set_title("Attendance and academic performance")
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)
        st.pyplot(fig)
        plt.close(fig)

    st.subheader("Average marks by risk level")
    risk_avg = filtered.groupby("risk_level", as_index=False)["marks"].mean()
    fig, ax = plt.subplots()
    ax.bar(risk_avg["risk_level"], risk_avg["marks"])
    ax.set_ylabel("Average marks")
    ax.set_ylim(0, 100)
    st.pyplot(fig)
    plt.close(fig)

with tab2:
    st.subheader("Student records")
    show_cols = ["student_id", "name", "attendance", "study_hours", "marks", "performance", "risk_level"]
    st.dataframe(filtered[show_cols].sort_values("marks"), use_container_width=True, hide_index=True)
    csv_bytes = filtered[show_cols].to_csv(index=False).encode("utf-8")
    st.download_button("⬇️ Download filtered report (CSV)", csv_bytes, "student_performance_report.csv", "text/csv")

with tab3:
    st.subheader("Students who may need support")
    high_risk = filtered[filtered["risk_level"] == "High"].sort_values("marks")
    if high_risk.empty:
        st.success("No high-risk students in the current filtered data.")
    else:
        st.warning(f"{len(high_risk)} student(s) are flagged as high risk by the project's rule-based indicator.")
        st.dataframe(high_risk[["student_id", "name", "attendance", "study_hours", "marks", "risk_level"]], use_container_width=True, hide_index=True)

    st.subheader("Try a simple performance estimate")
    st.caption("This is a transparent rule-based estimate for demonstration, not a validated machine-learning model or a guarantee of future results.")
    a, b = st.columns(2)
    with a:
        attendance_in = st.slider("Predicted student's attendance (%)", 0, 100, 80, key="pred_att")
    with b:
        hours_in = st.slider("Study hours per day", 0.0, 12.0, 2.0, 0.5, key="pred_hours")
    if attendance_in < 65 or hours_in < 1:
        estimate = "Needs focused support"
        explanation = "Low attendance or very limited study time suggests that extra support may help."
    elif attendance_in < 80 or hours_in < 2:
        estimate = "Moderate support recommended"
        explanation = "Improving attendance or consistent study time may help."
    else:
        estimate = "Positive study pattern"
        explanation = "The entered attendance and study time suggest a positive pattern, but actual marks depend on many factors."
    st.metric("Study-pattern estimate", estimate)
    st.write(explanation)

st.divider()
st.caption("Built with Python • Pandas • NumPy • Matplotlib • Streamlit | Demo data is synthetic and for learning only.")
