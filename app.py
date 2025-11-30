
import streamlit as st
import pandas as pd
import joblib
import numpy as np

st.set_page_config(page_title="AI-SERS Cancer Diagnosis", page_icon="🧬", layout="centered")

@st.cache_resource
def load_model():
    try:
        return joblib.load("cancer_diagnosis_model.pkl")
    except:
        return None

model = load_model()

st.title("🧬 AI-Based Metabolic Cancer Diagnosis")
st.info("Enter normalized expression scores derived from SERS spectra.")

def user_input_features():
    gly = st.slider('Glycolysis Score', 0.0, 15.0, 8.5)
    lip = st.slider('Lipid Synthesis Score', 0.0, 15.0, 7.2)
    nuc = st.slider('Nucleotide Metab. Score', 0.0, 15.0, 6.1)
    tca = st.slider('TCA Cycle Score', 0.0, 15.0, 9.4)
    data = {'Glikoliz': gly, 'Lipid_Sentezi': lip, 'Nukleotit': nuc, 'TCA_Dongusu': tca}
    return pd.DataFrame(data, index=[0])

input_df = user_input_features()

if st.button("🔍 Analyze"):
    if model:
        prediction = model.predict(input_df)[0]
        proba = model.predict_proba(input_df)
        st.subheader(f"Diagnosis: {prediction}")
        st.bar_chart(pd.DataFrame(proba, columns=model.classes_).T)
    else:
        st.error("Model file not found. Please upload 'cancer_diagnosis_model.pkl'.")
