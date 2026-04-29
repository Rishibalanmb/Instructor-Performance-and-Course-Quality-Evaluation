import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

st.set_page_config(page_title="🎓 EduPro Student Performance Dashboard", page_icon="📊", layout="wide")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv('EduPro_Clean_Master.csv')
    return df

df = load_data()

st.title("🎓 EduPro Student Performance Dashboard")
st.markdown("Interactive analytics for student metrics | Data Analyst Portfolio")

# Sidebar filters
st.sidebar.header("🔍 Filters")
grade_options = st.sidebar.multiselect("Grade Level", options=sorted(df['grade_level'].unique()), default=df['grade_level'].unique())
gender_options = st.sidebar.multiselect("Gender", options=df['gender'].unique(), default=df['gender'].unique())
school_options = st.sidebar.multiselect("School Type", options=df['school_type'].unique(), default=df['school_type'].unique())
involvement = st.sidebar.selectbox("Parental Involvement", ['All'] + sorted(df['parental_involvement'].unique()))

# Filter df
filtered_df = df[
    (df['grade_level'].isin(grade_options)) &
    (df['gender'].isin(gender_options)) &
    (df['school_type'].isin(school_options))
].copy()

if involvement != 'All':
    filtered_df = filtered_df[filtered_df['parental_involvement'] == involvement]

if filtered_df.empty:
    st.warning("No data matches filters. Reset to view defaults.")
    filtered_df = df

# KPIs Row 1
col1, col2, col3, col4, col5 = st.columns(5)
kpi1 = filtered_df['math_score'].mean()
kpi2 = filtered_df['reading_score'].mean()
kpi3 = filtered_df['science_score'].mean()
kpi4 = filtered_df['gpa'].mean()
kpi5 = filtered_df['attendance_rate'].mean()

col1.metric("📐 Avg Math", f"{kpi1:.1f}")
col2.metric("📖 Avg Reading", f"{kpi2:.1f}")
col3.metric("🔬 Avg Science", f"{kpi3:.1f}")
col4.metric("🎓 Avg GPA", f"{kpi4:.2f}")
col5.metric("📈 Avg Attendance", f"{kpi5:.1f}%")

# Charts Row 1
st.subheader("📊 Visualizations")

col_a, col_b = st.columns(2)

with col_a:
    fig_math, ax_math = plt.subplots()
    sns.histplot(data=filtered_df, x='math_score', hue='gender', kde=True, ax=ax_math)
    ax_math.set_title("Math Score Distribution")
    st.pyplot(fig_math)

with col_b:
    fig_gpa, ax_gpa = plt.subplots()
    sns.scatterplot(data=filtered_df, x='attendance_rate', y='gpa', hue='school_type', size='math_score', ax=ax_gpa)
    ax_gpa.set_title("Attendance vs GPA")
    st.pyplot(fig_gpa)

# Charts Row 2
col_c, col_d = st.columns(2)

with col_c:
    avg_by_grade = filtered_df.groupby('grade_level')[['math_score', 'reading_score', 'science_score']].mean()
    fig_bar, ax_bar = plt.subplots()
    avg_by_grade.plot(kind='bar', ax=ax_bar)
    ax_bar.set_title("Avg Scores by Grade")
    ax_bar.legend()
    plt.xticks(rotation=0)
    st.pyplot(fig_bar)

with col_d:
    corr_data = filtered_df[['math_score', 'reading_score', 'science_score', 'gpa', 'attendance_rate']].corr()
    fig_heatmap, ax_heat = plt.subplots(figsize=(8,6))
    sns.heatmap(corr_data, annot=True, cmap='coolwarm', center=0, ax=ax_heat)
    ax_heat.set_title("Correlations Heatmap")
    st.pyplot(fig_heatmap)

# Insights
st.subheader("💡 Insights")
high_gpa_count = (filtered_df['gpa'] >= 3.5).sum()
total = len(filtered_df)
st.success(f"High Performers (GPA ≥ 3.5): **{high_gpa_count}/{total} ({100*high_gpa_count/total:.1f}%)**")

invol_gpa = filtered_df.groupby('parental_involvement')['gpa'].mean().round(2)
fig_invol, ax_invol = plt.subplots()
invol_gpa.plot(kind='bar', ax=ax_invol)
ax_invol.set_title("Avg GPA by Parental Involvement")
ax_invol.set_ylabel("Avg GPA")
st.pyplot(fig_invol)
st.dataframe(invol_gpa)

# Data Table
with st.expander("📋 Raw Data Table"):
    st.dataframe(filtered_df)

st.markdown("---")
st.caption("✨ Portfolio-Ready | Streamlit + Pandas + Seaborn/Matplotlib")

