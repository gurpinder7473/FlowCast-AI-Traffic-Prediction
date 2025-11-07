import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title='Traffic Congestion Predictor', layout='centered')

st.title('Traffic Congestion Predictor (Neural-like Demo) 🚦')


st.sidebar.header("Input Controls")
hour = st.sidebar.slider("Hour of day", 0, 23, 8)
day = st.sidebar.selectbox("Day of week (0=Mon,...6=Sun)", list(range(7)), index=0)
is_weekend = 1 if day>=5 else 0
is_holiday = st.sidebar.checkbox("Holiday", value=False)
temperature = st.sidebar.number_input("Temperature (°C)", value=28.0, format="%0.2f")
precipitation = st.sidebar.number_input("Precipitation (mm)", value=0.0, format="%0.2f")
wind_speed = st.sidebar.number_input("Wind speed (km/h)", value=5.0, format="%0.2f")

def neural_like_predict(x):
    x = np.array(x, dtype=float)
    x_norm = np.array([x[0]/23.0, x[1]/6.0, x[2], x[3], (x[4]-10)/30.0, x[5]/50.0, x[6]/30.0])

    W1 = np.array([
        [1.2, -0.5, 0.0, 0.0, -0.4, 1.0, 0.1],
        [0.8, -0.2, -0.3, -0.5, 0.2, 0.9, 0.05],
        [0.5, -0.1, 0.2, -0.1, 0.1, 0.6, -0.2]
    ])
    b1 = np.array([0.2, -0.1, 0.0])
    h = np.tanh(W1.dot(x_norm) + b1)

    W2 = np.array([20.0, 25.0, 10.0])
    b2 = 30.0
    score = W2.dot(h) + b2

    score += x[5] * 1.2
    score -= x[2]*8.0
    score -= x[3]*18.0

    return max(0.0, min(100.0, score))

if st.button("Predict Congestion"):
    inp = [hour, day, is_weekend, int(is_holiday), temperature, precipitation, wind_speed]
    pred = neural_like_predict(inp)
    st.metric("Predicted Congestion (%)", f"{pred:.2f}%")

    fig, ax = plt.subplots(figsize=(6,1.2))
    ax.barh([0],[pred], height=0.6)
    ax.set_xlim(0,100)
    ax.set_yticks([])
    ax.set_xlabel("Congestion (%)")
    ax.set_title("Predicted Traffic Congestion")
    for spine in ax.spines.values():
        spine.set_visible(False)
    st.pyplot(fig)

    if pred < 25:
        st.success("Traffic Status: LOW ✅")
    elif pred < 50:
        st.info("Traffic Status: MODERATE ⚠️")
    elif pred < 75:
        st.warning("Traffic Status: HIGH 🚧")
    else:
        st.error("Traffic Status: SEVERE 🚨")

st.write('---')
st.subheader("Sample Data (Synthetic)")    

try:
    df = pd.read_csv("data/traffic_synthetic.csv")
    st.dataframe(df.head(10))
except:
    st.write("No sample dataset found.")
