import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as font_obj

st.set_page_config(
    page_title="PNEUMA-Shield | SIH26115 Digital Twin",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🛡️ PNEUMA-SHIELD: SIH26115 Software Edition Prototype")
st.caption("Uncertainty-Aware Chem-Optical Verification & Bio-Hazard Airlock Simulator")

# Sidebar Test Selector
st.sidebar.header("SIH Judge Test Suite")
scenario = st.sidebar.radio(
    "Select Waste Test Scenario:",
    ["Yellow Bag (Soiled Gauze)", "Red Bag (Recyclable Plastics)", "HAZARD: Syringe in Red Bag (AI Abstain)", "VOC Off-Gas Leak"]
)

# Telemetry data dictionary
telemetry_db = {
    "Yellow Bag (Soiled Gauze)": {
        "mass": 450, "vol": 530, "density": 0.85, "voc": 45, "temp": 31.4, "inductive": "ABSENT",
        "entropy": 0.18, "category": "YELLOW (INCINERATION)", "status": "ACCEPT", "conf": "96.4%"
    },
    "Red Bag (Recyclable Plastics)": {
        "mass": 180, "vol": 820, "density": 0.22, "voc": 18, "temp": 28.1, "inductive": "ABSENT",
        "entropy": 0.12, "category": "RED (AUTOCLAVE/RECYCLE)", "status": "ACCEPT", "conf": "98.1%"
    },
    "HAZARD: Syringe in Red Bag (AI Abstain)": {
        "mass": 320, "vol": 410, "density": 0.78, "voc": 65, "temp": 34.8, "inductive": "DETECTED (SHARPS)",
        "entropy": 0.68, "category": "AI ABSTAIN (HAZARD FLAGGED)", "status": "ABSTAIN", "conf": "42.0%"
    },
    "VOC Off-Gas Leak": {
        "mass": 510, "vol": 600, "density": 0.85, "voc": 295, "temp": 38.2, "inductive": "ABSENT",
        "entropy": 0.54, "category": "AI ABSTAIN (VOC SPIKE)", "status": "ABSTAIN", "conf": "51.2%"
    }
}

data = telemetry_db[scenario]

col1, col2, col3 = st.columns([4, 4, 4])

with col1:
    st.subheader("📦 Airlock Multi-Sensor Telemetry")
    st.metric("Mass Density", f"{data['density']} g/cm³")
    st.metric("Thermal Temp", f"{data['temp']} °C")
    st.metric("VOC Gas Off-Gas", f"{data['voc']} ppm")
    st.metric("Inductive Needle Sensor", data['inductive'])

with col2:
    st.subheader("🧠 Conformal AI Abstention Engine")
    st.write(f"**Softmax Uncertainty Entropy H(x):** `{data['entropy']}` / Threshold τ=0.42")
    st.progress(min(1.0, data['entropy'] / 0.8))
    
    if data['status'] == 'ABSTAIN':
        st.error("🚨 **AI ABSTENTION TRIGGERED!** Solenoid Lock Engaged!")
        st.warning("Reason: Model Uncertainty Entropy H(x) >= 0.42. Physical Drop Gate Locked.")
    else:
        st.success(f"✅ Verified Category: **{data['category']}**")
        st.info(f"Model Confidence: {data['conf']}")

with col3:
    st.subheader("🔒 Solenoid Interlock Gate Status")
    if data['status'] == 'ABSTAIN':
        st.markdown("<h2 style='color:red;'>🔒 SOLENOID LOCKED</h2>", unsafe_allow_html=True)
        st.button("Human Override -> Route to Sharps Vault")
    else:
        st.markdown("<h2 style='color:green;'>🔓 UNLOCKED / ROUTED</h2>", unsafe_allow_html=True)

st.divider()
st.subheader("📊 Live Hospital Control Room Digital Twin")
chart_data = pd.DataFrame({
    'Ward': ['ICU 01', 'ICU 02', 'OT 03', 'Ward 04', 'Emergency'],
    'Waste Volume (kg)': [42, 38, 65, 20, 55],
    'Bio-Hazard Score': [85, 90, 95, 30, 88]
})
fig = px.bar(chart_data, x='Ward', y='Waste Volume (kg)', color='Bio-Hazard Score', title="Real-Time Hospital Ward Bio-Hazard Dynamics")
st.plotly_chart(fig, use_container_width=True)
