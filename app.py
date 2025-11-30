import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import os

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="AI-SERS Cancer Diagnosis", page_icon="🧬", layout="centered")

# --- MODEL VE VERİ YÜKLEME (CACHE) ---
@st.cache_resource
def get_model_and_data():
    # Dosya adını kontrol et (GitHub'daki adıyla birebir aynı olmalı)
    file_name = "metabolic_scores_final.csv"
    
    # 1. Dosya Var mı Kontrolü
    if not os.path.exists(file_name):
        return None, f"HATA: '{file_name}' dosyası bulunamadı. Lütfen GitHub reponuza bu dosyayı yükleyin."
    
    try:
        # 2. Veriyi Oku
        df = pd.read_csv(file_name)
        
        # Gereksiz sütun temizliği
        if 'Sample' in df.columns:
            df = df.drop(columns=['Sample'])
            
        X = df.drop(columns=['Cancer'])
        y = df['Cancer']
        
        # 3. Modeli Eğit (Anlık Eğitim - En Garantisi)
        model = RandomForestClassifier(n_estimators=200, random_state=42)
        model.fit(X, y)
        
        return model, None # Hata yok
        
    except Exception as e:
        return None, f"Veri okunurken hata oluştu: {e}"

# Modeli Yükle
model, error_message = get_model_and_data()

# --- BAŞLIK ---
st.title("🧬 AI-Based Metabolic Cancer Diagnosis")

# --- HATA VARSA GÖSTER, YOKSA DEVAM ET ---
if error_message:
    st.error(error_message)
    st.info("İpucu: GitHub reponuzda 'metabolic_scores_final.csv' dosyasının olduğundan emin olun.")
else:
    st.success("Model başarıyla eğitildi ve hazır! ✅")
    
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

# --- ALT BİLGİ ---
st.divider()
st.caption("Developed for ML Bootcamp Capstone Project")
