import streamlit as st
import numpy as np

st.set_page_config(page_title="NDLVC-5y Risk Score", layout="centered")

st.title("NDLVC-5y Risk Score Calculator")
st.markdown("Calculate the 5-year risk of major arrhythmic events (MAE) in non-dilated LV cardiomyopathy.")

# Input
male = st.checkbox("Male sex")
lvef_low = st.checkbox("Left ventricular ejection fraction (LVEF) < 45%")
nsvt = st.checkbox("Non-sustained ventricular tachycardia (NSVT)")
septal_lge = st.checkbox("Septal late gadolinium enhancement (LGE)")
ring_lge = st.checkbox("Ring-like pattern LGE")
pvs_hr = st.checkbox("Pathogenic/likely pathogenic variant in high-risk genes (LMNA, FLNC, TMEM43, PLN, DSP, RBM20)")
minfl = st.checkbox("Myocardial inflammation (by EMB or T2w CMR)")

# Compute Prognostic Index (PI)
pi = (
    0.8605 * male +
    1.6967 * lvef_low +
    1.1288 * nsvt +
    0.6929 * septal_lge +
    0.2275 * ring_lge +
    1.5336 * pvs_hr +
    2.7535 * minfl
)

# Calculate risk
baseline_survival = 0.99600731958437
risk = 1 - (baseline_survival ** np.exp(pi))
risk_pct = round(100 * risk, 1)

# Classify risk
if risk < 0.05:
    risk_class = "Class 1: Low risk (<5%)"
elif risk < 0.20:
    risk_class = "Class 2: Mid-low risk (5–20%)"
elif risk < 0.40:
    risk_class = "Class 3: Mid-high risk (20–40%)"
else:
    risk_class = "Class 4: High risk (>40%)"

# Output
st.markdown("### Results")
st.metric(label="Estimated 5-year risk of MAE", value=f"{risk_pct}%")
st.markdown(f"**Risk Class:** {risk_class}")
