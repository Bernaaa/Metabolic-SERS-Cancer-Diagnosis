import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import os

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="AI-SERS Cancer Diagnosis", page_icon="🧬", layout="centered")

# --- HATA AYIKLAMA MODU: Dosya Kontrolü ---
st.write("📂 Çalışma Dizini:", os.getcwd())
dosya_adi = "metabolic_scores_final.csv"

if not os.path.exists(dosya_adi):
    st.error(f"❌ KRİTİK HATA: '{dosya_adi}' dosyası bulunamadı!")
    st.info("Lütfen GitHub reponuzda bu dosyanın 'app.py' ile aynı yerde olduğundan emin olun.")
    st.stop() # Dosya yoksa uygulamayı durdur

# --- MODEL VE VERİ YÜKLEME ---
@st.cache_resource
def get_model_and_data():
    try:
        # 1. Veriyi Oku
        df = pd.read_csv(dosya_adi)
        
        # Gereksiz sütun temizliği
        if 'Sample' in df.columns:
            df = df.drop(columns=['Sample'])
            
        X = df.drop(columns=['Cancer'])
        y = df['Cancer']
        
        # 2. Modeli Eğit (Anlık Eğitim - En Garantisi)
        model = RandomForestClassifier(n_estimators=200, random_state=42)
        model.fit(X, y)
        
        return model
        
    except Exception as e:
        return None

model = get_model_and_data()

if model is None:
    st.error("Veri okunamadığı veya model eğitilemediği için uygulama çalışmıyor.")
    st.stop()

# --- BAŞLIK ---
st.title("🧬 AI-Based Metabolic Cancer Diagnosis")
st.success("Sistem Hazır ve Çalışıyor! ✅")

# --- GİRİŞ PANELİ ---
st.sidebar.header("Patient Metabolic Profile")

def user_input_features():
    gly = st.sidebar.slider('Glycolysis Score', 0.0, 15.0, 8.5)
    lip = st.sidebar.slider('Lipid Synthesis Score', 0.0, 15.0, 7.2)
    nuc = st.sidebar.slider('Nucleotide Metab. Score', 0.0, 15.0, 6.1)
    tca = st.sidebar.slider('TCA Cycle Score', 0.0, 15.0, 9.4)
    
    data = {'Glikoliz': gly, 'Lipid_Sentezi': lip, 'Nukleotit': nuc, 'TCA_Dongusu': tca}
    return pd.DataFrame(data, index=[0])

input_df = user_input_features()

# --- TAHMİN ---
if st.button("🔍 Analyze & Diagnose"):
    # Tahmin ve Olasılık
    prediction = model.predict(input_df)[0]
    prediction_proba = model.predict_proba(input_df)
    
    st.divider()
    st.subheader(f"Diagnosis: {prediction}")
    
    # Olasılık Grafiği
    prob_df = pd.DataFrame(prediction_proba, columns=model.classes_)
    st.bar_chart(prob_df.T)
    
    # Yorumlar
    if prediction == "PAAD":
        st.warning("⚠️ High Risk: Pancreatic Adenocarcinoma detected.")
    elif prediction == "OV":
        st.info("ℹ️ Detection: Ovarian Cancer signature.")
    else:
        st.success("✅ Detection: Cholangiocarcinoma signature.")

st.divider()
st.caption("Developed for ML Bootcamp Capstone Project")
