import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="NDLVC-5y Risk Score", layout="centered")

st.title("NDLVC-5y Risk Score Calculator")
st.markdown("Estimate the 5-year risk of major arrhythmic events (MAE) in patients with non-dilated LV cardiomyopathy.")

# Input
male = st.checkbox("Male sex")
lvef_low = st.checkbox("LVEF < 45%")
nsvt = st.checkbox("Non-sustained VT")
septal_lge = st.checkbox("Septal LGE")
ring_lge = st.checkbox("Ring-like pattern LGE")
pvs_hr = st.checkbox("PVs/LPVs in high-risk genes (LMNA, FLNC, TMEM43, PLN, DSP, RBM20)")
minfl = st.checkbox("Myocardial inflammation (by EMB or T2w CMR)")

# Calculate Prognostic Index
pi = (
    0.8605 * male +
    1.6967 * lvef_low +
    1.1288 * nsvt +
    0.6929 * septal_lge +
    0.2275 * ring_lge +
    1.5336 * pvs_hr +
    2.7535 * minfl
)

baseline_survival = 0.99600731958437
risk = 1 - (baseline_survival ** np.exp(pi))
risk_pct = round(100 * risk, 1)

# Classify
if risk < 5:
    risk_class = "Class 1: Low risk (<5%)"
    class_color = "🟢"
elif risk < 20:
    risk_class = "Class 2: Mid-low risk (5–20%)"
    class_color = "🟡"
elif risk < 40:
    risk_class = "Class 3: Mid-high risk (20–40%)"
    class_color = "🟠"
else:
    risk_class = "Class 4: High risk (>40%)"
    class_color = "🔴"

# Output
st.markdown("### Results")
st.metric(label="Estimated 5-year risk of MAE", value=f"{risk_pct}%", delta=risk_class)

st.markdown(f"**Risk Class:** {class_color} {risk_class}")

# Graph
classes = ['Class 1\n<5%', 'Class 2\n5–20%', 'Class 3\n20–40%', 'Class 4\n>40%']
colors = ['green', 'yellow', 'orange', 'red']
bars = [5, 20, 40, 60]

fig, ax = plt.subplots(figsize=(8, 4))
ax.bar(classes, bars, color=colors, edgecolor='black')
ax.axhline(risk_pct, color='black', linestyle='--', linewidth=2)
ax.text(3.2, risk_pct + 1, f"Patient: {risk_pct:.1f}%", ha='right', fontsize=10, fontweight='bold')
ax.set_ylim(0, 70)
ax.set_ylabel("5-year Risk (%)")
ax.set_title("NDLVC-5y Risk Classes")
ax.spines[['right', 'top']].set_visible(False)

st.pyplot(fig)
