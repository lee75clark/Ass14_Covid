
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="COVID-19 Global Dashboard", layout="wide")
st.title("COVID-19 Global Dashboard")
st.caption("Historical worldwide aggregate data with a simple 30-day forecast.")

DATA_PATH = "data/processed_with_predictions.csv"

@st.cache_data
def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path, parse_dates=["date"])
    return df.sort_values("date")


df = load_data(DATA_PATH)
historical = df[df["prediction_flag"] == 0].copy()
forecast = df[df["prediction_flag"] == 1].copy()

min_date, max_date = historical["date"].min(), df["date"].max()
selected_dates = st.sidebar.date_input(
    "Date range",
    value=(min_date.date(), historical["date"].max().date()),
    min_value=min_date.date(),
    max_value=max_date.date(),
)

if isinstance(selected_dates, tuple) and len(selected_dates) == 2:
    start_date, end_date = pd.to_datetime(selected_dates[0]), pd.to_datetime(selected_dates[1])
else:
    start_date, end_date = min_date, historical["date"].max()

filtered_hist = historical[(historical["date"] >= start_date) & (historical["date"] <= end_date)]

c1, c2, c3, c4 = st.columns(4)
latest_hist = historical.iloc[-1]
with c1:
    st.metric("Confirmed", f"{int(latest_hist['confirmed']):,}")
with c2:
    st.metric("Recovered", f"{int(latest_hist['recovered']):,}")
with c3:
    st.metric("Deaths", f"{int(latest_hist['deaths']):,}")
with c4:
    st.metric("Active Cases", f"{int(latest_hist['active_cases']):,}")

st.subheader("1) Historical confirmed cases")
fig1, ax1 = plt.subplots(figsize=(10, 4))
ax1.plot(filtered_hist["date"], filtered_hist["confirmed"])
ax1.set_xlabel("Date")
ax1.set_ylabel("Confirmed Cases")
st.pyplot(fig1)

st.subheader("2) Daily new confirmed cases")
fig2, ax2 = plt.subplots(figsize=(10, 4))
ax2.plot(filtered_hist["date"], filtered_hist["daily_new_confirmed"])
ax2.set_xlabel("Date")
ax2.set_ylabel("Daily New Cases")
st.pyplot(fig2)

st.subheader("3) Cumulative outcomes")
fig3, ax3 = plt.subplots(figsize=(10, 4))
ax3.plot(filtered_hist["date"], filtered_hist["recovered"], label="Recovered")
ax3.plot(filtered_hist["date"], filtered_hist["deaths"], label="Deaths")
ax3.legend()
ax3.set_xlabel("Date")
ax3.set_ylabel("Count")
st.pyplot(fig3)

st.subheader("4) 30-day forecast for confirmed cases")
fig4, ax4 = plt.subplots(figsize=(10, 4))
ax4.plot(historical["date"], historical["confirmed"], label="Historical")
if not forecast.empty:
    ax4.plot(forecast["date"], forecast["predicted_confirmed"], label="Forecast")
ax4.legend()
ax4.set_xlabel("Date")
ax4.set_ylabel("Confirmed Cases")
st.pyplot(fig4)

st.dataframe(df.tail(20), use_container_width=True)
