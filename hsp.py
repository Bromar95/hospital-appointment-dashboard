import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# Page setup (must be the first Streamlit command)
st.set_page_config(page_title="Hospital Appointment Analytics", page_icon="🏥", layout="wide")

# Consistent colors for each status across every chart
STATUS_COLORS = {"Attended": "#2E9E6B", "No-Show": "#D64545", "Cancelled": "#9AA0A6"}
STATUS_ORDER = ["Attended", "No-Show", "Cancelled"]


# Load Dataset
# Path(__file__).parent is the folder this script lives in (datasets/),
# so the CSV is found no matter which folder you run Streamlit from.
@st.cache_data
def load_data():
    csv_path = Path(__file__).parent / "hospital_appointments.csv"
    df = pd.read_csv(csv_path)
    df['date'] = pd.to_datetime(df['date'])
    df['weekday'] = df['date'].dt.day_name()
    df['week'] = df['date'].dt.to_period('W').apply(lambda r: r.start_time)
    df['age_group'] = pd.cut(
        df['patient_age'],
        bins=[0, 17, 39, 64, 120],
        labels=["0-17", "18-39", "40-64", "65+"],
        include_lowest=True
    )
    return df


df = load_data()


# Sidebar Filters
st.sidebar.header("Filters")

# Date range filter
min_date = df['date'].min().date()
max_date = df['date'].max().date()
date_range = st.sidebar.date_input(
    "Select Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

# Handles the moment when only the start date has been clicked
if isinstance(date_range, (list, tuple)) and len(date_range) == 2:
    start_date, end_date = date_range
else:
    st.sidebar.warning("Pick an end date to complete the range.")
    st.stop()

# Clinic filter: choose one, several, or all clinics
clinics = sorted(df['department'].unique().tolist())
selected_clinics = st.sidebar.multiselect("Select Clinics", clinics, default=clinics)

# Status filter
selected_status = st.sidebar.multiselect("Select Status", STATUS_ORDER, default=STATUS_ORDER)


# Apply Filters
filtered_df = df[
    (df['date'] >= pd.to_datetime(start_date)) &
    (df['date'] <= pd.to_datetime(end_date)) &
    (df['department'].isin(selected_clinics)) &
    (df['status'].isin(selected_status))
]

if filtered_df.empty:
    st.warning("No appointments match these filters. Try widening them.")
    st.stop()


# Dashboard Title
st.title("🏥 Hospital Appointment Analytics Dashboard")
st.write(f"Showing {len(filtered_df)} appointments from **{start_date}** to **{end_date}**")


# KPI Summary Row
total = len(filtered_df)
attended = (filtered_df['status'] == "Attended").sum()
no_shows = (filtered_df['status'] == "No-Show").sum()
cancelled = (filtered_df['status'] == "Cancelled").sum()

k1, k2, k3, k4 = st.columns(4)
k1.metric("Total Appointments", f"{total}")
k2.metric("Attendance Rate", f"{attended / total:.1%}")
k3.metric("No-Show Rate", f"{no_shows / total:.1%}")
k4.metric("Cancellation Rate", f"{cancelled / total:.1%}")

st.divider()


# 1. Total Appointments per Day & Week
st.subheader("📅 Total Appointments Over Time")

col1, col2 = st.columns(2)

# Daily, with a 7-day rolling average to smooth out the noise
daily_df = filtered_df.groupby('date').size().reset_index(name='appointments')
daily_df['7-day average'] = daily_df['appointments'].rolling(7, min_periods=1).mean()
fig_daily = px.line(
    daily_df, x='date', y=['appointments', '7-day average'],
    title="Appointments per Day"
)
fig_daily.update_layout(legend_title_text="", yaxis_title="appointments")
col1.plotly_chart(fig_daily, width="stretch")

# Weekly, stacked by status so attendance trends are visible
weekly_df = filtered_df.groupby(['week', 'status']).size().reset_index(name='appointments')
fig_weekly = px.bar(
    weekly_df, x='week', y='appointments', color='status',
    title="Appointments per Week by Status",
    color_discrete_map=STATUS_COLORS,
    category_orders={"status": STATUS_ORDER}
)
col2.plotly_chart(fig_weekly, width="stretch")

# Day-of-week pattern
weekday_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
weekday_df = filtered_df.groupby(['weekday', 'status']).size().reset_index(name='appointments')
fig_weekday = px.bar(
    weekday_df, x='weekday', y='appointments', color='status',
    title="Appointments by Day of Week",
    color_discrete_map=STATUS_COLORS,
    category_orders={"weekday": weekday_order, "status": STATUS_ORDER}
)
st.plotly_chart(fig_weekday, width="stretch")

st.divider()


# 2. No-Show vs Attended Rate
st.subheader("👥 Attendance Status Overview")

col3, col4 = st.columns(2)

status_df = filtered_df['status'].value_counts().reset_index()
status_df.columns = ['status', 'count']
fig_status = px.pie(
    status_df, names='status', values='count',
    title="Appointment Status Distribution",
    color='status', color_discrete_map=STATUS_COLORS, hole=0.4
)
col3.plotly_chart(fig_status, width="stretch")

# No-show rate by age group
age_df = (
    filtered_df.groupby('age_group', observed=False)['status']
    .apply(lambda s: (s == "No-Show").mean() * 100)
    .reset_index(name='no_show_rate')
)
fig_age = px.bar(
    age_df, x='age_group', y='no_show_rate',
    title="No-Show Rate by Age Group (%)",
    text=age_df['no_show_rate'].round(1),
    color_discrete_sequence=[STATUS_COLORS["No-Show"]]
)
fig_age.update_layout(yaxis_title="no-show rate (%)", xaxis_title="age group")
col4.plotly_chart(fig_age, width="stretch")

st.divider()


# 3. Compare Clinics
st.subheader("🏥 Clinic Comparison")

col5, col6 = st.columns(2)

# Volume by clinic, stacked by status
clinic_status_df = filtered_df.groupby(['department', 'status']).size().reset_index(name='count')
fig_clinic = px.bar(
    clinic_status_df, x='department', y='count', color='status',
    title="Appointments by Clinic and Status",
    color_discrete_map=STATUS_COLORS,
    category_orders={"status": STATUS_ORDER}
)
col5.plotly_chart(fig_clinic, width="stretch")

# No-show rate by clinic, sorted so the worst clinic is on top
clinic_rate_df = (
    filtered_df.groupby('department')['status']
    .apply(lambda s: (s == "No-Show").mean() * 100)
    .reset_index(name='no_show_rate')
    .sort_values('no_show_rate')
)
fig_rate = px.bar(
    clinic_rate_df, x='no_show_rate', y='department', orientation='h',
    title="No-Show Rate by Clinic (%)",
    text=clinic_rate_df['no_show_rate'].round(1),
    color_discrete_sequence=[STATUS_COLORS["No-Show"]]
)
fig_rate.update_layout(xaxis_title="no-show rate (%)", yaxis_title="")
col6.plotly_chart(fig_rate, width="stretch")

# Summary table for each clinic
summary = filtered_df.groupby('department').agg(
    appointments=('appointment_id', 'count'),
    attended=('status', lambda s: (s == "Attended").sum()),
    no_shows=('status', lambda s: (s == "No-Show").sum()),
    cancelled=('status', lambda s: (s == "Cancelled").sum()),
    avg_age=('patient_age', 'mean')
)
summary['no_show_rate_%'] = (summary['no_shows'] / summary['appointments'] * 100).round(1)
summary['avg_age'] = summary['avg_age'].round(1)
st.dataframe(summary.sort_values('appointments', ascending=False), width="stretch")

st.divider()


# Raw data and download
with st.expander("🔍 View filtered data"):
    st.dataframe(
        filtered_df[['appointment_id', 'date', 'department', 'patient_age', 'gender', 'status']],
        width="stretch"
    )

st.download_button(
    "⬇️ Download filtered data as CSV",
    data=filtered_df.to_csv(index=False).encode('utf-8'),
    file_name="filtered_appointments.csv",
    mime="text/csv"
)

st.info("Use the filters on the left to interact with the dashboard!")