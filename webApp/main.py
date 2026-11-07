import streamlit as st
import requests
import pandas as pd
import os
from dotenv import load_dotenv
import time

load_dotenv()
PROMETHEUS_URL = os.getenv("PROMETHEUS_URL")

ENDPOINT = f'{PROMETHEUS_URL}/api/v1/query'


def get_data(query: str, time_period : str):
    time_labels = {
        "1d":[1,"5m"],
        "7d":[7,"30m"],
        "1y":[365,"4h"],
    }

    end_time = int(time.time())
    start_time = end_time - (time_labels[time_period][0] * 24 * 60 * 60)



    step = time_labels[time_period][1]

    params = {
        # average of the raw samples inside each step window
        "query": f"avg_over_time({query}[{step}])",
        "start": start_time,
        "end": end_time,
        "step": step
    }

    response = requests.get(ENDPOINT+"_range", params=params)
    data = response.json()

    if data['status'] == 'success':
        results = data['data']['result']
        for metrics in results:

            for metric_name, metric_value in metrics.items():


                for value in metric_value:
                    pass

        return results
    else:
        print("Query failed:", data)
        st.error(f"Prometheus query failed: {data.get('error')}")
        st.stop()
def get_latest_value(query: str):
    response = requests.get(ENDPOINT, params={'query': query})
    data = response.json()

    return data['data']['result'][0]['value'][1]

st.set_page_config(
    page_title="Pogoda w Krakowie",      # Sets the browser tab title
    page_icon= "☀",                   # Sets the favicon (emoji, image path, or URL)
    layout="wide"                     # Optional: Choose "centered" or "wide"
)


st.set_option("client.toolbarMode", "viewer")
st.title("Pogoda w Krakowie")

col1, col2 = st.columns(2)
col1.metric("Temperatura", get_latest_value(query="weather_temperature") + "°C")
col2.metric("Wilgotność", get_latest_value(query="weather_humidity") + "%")





time_period_from_button = st.radio(
    "wybierz przedział czasu:",
    ["1 dzień", "tydzień", "rok"],
    horizontal=True
)
time_labels = {
    "1 dzień":"1d",
    "tydzień":"7d",
    "rok":"1y",
}
time_period = str(time_labels[time_period_from_button])

st.subheader("Wilgotność")

humidity = get_data(query="weather_humidity", time_period=time_period)[0]
df = pd.DataFrame(humidity['values'], columns=['Time', 'Humidity'])
df['Humidity'] = df['Humidity'].astype(float)
df['Time'] = pd.to_datetime(df['Time'], unit='s')
df.set_index('Time', inplace=True)

st.line_chart(df)

st.subheader("Temperatura")

temperature = get_data(query="weather_temperature", time_period=time_period)[0]
df = pd.DataFrame(temperature['values'], columns=['Time', 'Temperature'])
df['Temperature'] = df['Temperature'].astype(float)
df['Time'] = pd.to_datetime(df['Time'], unit='s')
df.set_index('Time', inplace=True)

st.line_chart(df)

