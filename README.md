# 🏥 Hospital Appointment Analytics Dashboard with Streamlit

🚀 **Live App:** [hospital-appointments-omar.streamlit.app](https://hospital-appointments-omar.streamlit.app/)

## 📌 Project Overview

This project is an interactive dashboard built in Python and Streamlit to analyze hospital appointment data. It uses 300 appointments from January to March 2025 across six clinics, with patient age, gender, department, date, and appointment status (Attended, No-Show, or Cancelled).

The base dashboard charts appointments over time, shows the status breakdown, and ranks clinics by volume. I then expanded it to answer the questions a clinic manager would actually ask: which clinics and patient groups miss the most appointments, and how attendance changes week to week. I added rate-based KPIs, no-show rates by clinic and age group, status-split trend charts, a clinic summary table, multi-select filters, and CSV export. I also audited the data for clinical plausibility and found that most Pediatrics patients are adults.

## 🎯 Key Features

✅ KPI Summary: Shows total appointments plus attendance, no-show, and cancellation rates that update with every filter.  
✅ Daily Trend: Plots appointments per day with a 7-day rolling average to smooth daily noise.  
✅ Weekly Trend by Status: Stacks each week's appointments by Attended, No-Show, and Cancelled.  
✅ Day-of-Week Pattern: Compares appointment volume and status across the days of the week.  
✅ Status Distribution: Shows the overall share of each appointment outcome in a donut chart.  
✅ No-Show Rate by Age Group: Compares missed appointments across four age bands.  
✅ No-Show Rate by Clinic: Ranks clinics by the share of appointments missed, not just raw counts.  
✅ Clinic Summary Table: Lists volume, each status, average age, and no-show rate for every clinic.  
✅ Interactive Filters: Filters by date range, one or more clinics, and appointment status.  
✅ Data Export: Lets users view the filtered records and download them as a CSV.  

## 🗂️ Repository Files

| File | Description |
|---|---|
| `hsp.py` | Streamlit app that builds the interactive dashboard |
| `hospital_appointments.csv` | Raw dataset: 300 rows and 6 columns of appointment records |
| `requirements.txt` | Packages used to deploy the app |

## 🧹 Data Preparation

- Loaded the data with `pd.read_csv()` using a path relative to the script, so the app runs on any computer and on Streamlit Cloud.
- Confirmed the dataset has no missing values and no duplicate rows.
- Converted `date` to a datetime column with `pd.to_datetime()`.
- Added `weekday` and `week` columns to support the day-of-week and weekly charts.
- Grouped patient age into four bands with `pd.cut()`: 0-17, 18-39, 40-64, and 65+.
- Cached the loaded data with `@st.cache_data` so filters respond quickly.
- **Flagged a clinical plausibility issue.** 38 of the 48 Pediatrics patients (79%) are 18 or older, and the oldest is 89. Appointments also fall evenly across weekends and weekdays. Both point to synthetic practice data, so clinic-level and age-level results should be read as a demonstration of the method, not as real clinical findings.

## 🛠️ Skills & Tools Applied

- Language and Environment: Python, Visual Studio Code
- Libraries: pandas, Plotly Express, Streamlit
- Analysis: Grouping and aggregation, rate calculation, rolling averages, age binning
- Visualization: Line, stacked bar, horizontal bar, and donut charts with consistent status colors
- App Development: Sidebar filters, KPI metrics, multi-column layout, data caching, CSV download
- Deployment: GitHub and Streamlit Community Cloud
- Clinical Knowledge: Data plausibility checks, appointment adherence metrics

## 📈 Business Questions Answered

This project provides insights into:

- How many appointments does the hospital handle each day and week?
- What share of appointments end in a no-show or cancellation?
- Which clinics have the highest no-show rates?
- Do no-show rates differ by patient age?
- Which days of the week see the most missed appointments?
- Is the data clinically plausible?

## 💡 Key Insights

### Overall Attendance

- Of 300 appointments, **208 were attended (69.3%)**, **63 were no-shows (21.0%)**, and **29 were cancelled (9.7%)**.
- About **1 in 5 appointments was missed** without cancelling, which is the main gap the dashboard is built to track.
- The hospital averaged **3.4 appointments per day** and about **21 per week**. The final week contains only March 31, so its low count reflects a partial week, not a real drop.

### Clinic Comparison

| Clinic | Appointments | Attended | No-Show Rate | Cancellation Rate |
|---|---|---|---|---|
| General Medicine | 64 | 65.6% | 25.0% | 9.4% |
| Cardiology | 57 | 70.2% | 19.3% | 10.5% |
| Pediatrics | 48 | 64.6% | 27.1% | 8.3% |
| Orthopedics | 47 | 74.5% | 14.9% | 10.6% |
| Dermatology | 43 | 67.4% | 18.6% | 14.0% |
| ENT | 41 | 75.6% | 19.5% | 4.9% |

- **Pediatrics (27.1%)** and **General Medicine (25.0%)** had the highest no-show rates.
- **Orthopedics** had the lowest no-show rate at **14.9%**, and **ENT** had the highest attendance at **75.6%**.
- **Dermatology** had the highest cancellation rate at **14.0%**, nearly three times ENT's **4.9%**.
- General Medicine had the most appointments (64), which shows why rates matter more than counts: a busy clinic will always have more no-shows.

### Patient Patterns

- No-show rates **fell steadily with age**: **28.1%** for ages 0-17, **21.9%** for 18-39, **18.4%** for 40-64, and **17.1%** for 65+.
- **Thursday** had the highest no-show rate (**26.2%**) and **Wednesday** the lowest (**14.6%**).
- **February** had the highest monthly no-show rate at **27.0%**, compared with about **18%** in January and March.

### Limitations

- With only 41 to 64 appointments per clinic, a few missed visits can shift a rate by several points. These differences would need a larger dataset to confirm.
- The Pediatrics age issue means the clinic and age-group findings describe this practice dataset, not real hospital behavior.

## 🚀 Learning Outcomes

Building this project strengthened my skills in:

📌 Building an interactive dashboard with Streamlit  
📌 Turning raw counts into rates that allow fair comparison across groups  
📌 Designing filters that update every chart and metric at once  
📌 Using consistent colors so status reads the same across every chart  
📌 Checking a dataset for clinical plausibility before trusting the results  
📌 Deploying a Python app to the web with GitHub and Streamlit Community Cloud  

## 🔮 Next Steps

- Test whether no-show differences between clinics and age groups are statistically significant.
- Add lead time between booking and appointment, a known driver of no-shows.
- Build a model to predict which appointments are likely to be missed.
- Apply the dashboard to a larger, real-world appointment dataset.

## 🙌 Acknowledgment

This project taught me that a dashboard is only as useful as the questions it answers. Asking which clinics and patients miss the most visits, and whether the data itself makes clinical sense, turned it into a tool a clinic manager could act on.

## 👨‍💻 Author

**Omar Shazley:** Data Analyst | Python, Excel, SQL, and healthcare data analytics

💼 [LinkedIn](ADD-LINKEDIN-LINK-HERE)  
💻 [GitHub Portfolio](https://github.com/Bromar95)  
📧 Email: [omarshazley@gmail.com](mailto:omarshazley@gmail.com)

✨ If you like this project, don't forget to ⭐ star the repo!
