import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import os

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="AI-SERS Cancer Diagnosis", page_icon="🧬")

# --- BAŞLIK ---
st.title("🧬 AI-Based Metabolic Cancer Diagnosis")

# --- 1. DOSYAYI BUL VE OKU ---
# Cache kullanmıyoruz, her seferinde taze okusun.
file_name = "metabolic_scores_final.csv"
file_path = None

# Dosyayı ara
if os.path.exists(file_name):
    file_path = file_name
else:
    for root, dirs, files in os.walk("."):
        if file_name in files:
            file_path = os.path.join(root, file_name)
            break

if file_path is None:
    st.error(f"🚨 HATA: '{file_name}' dosyası bulunamadı. Lütfen GitHub'da dosya adının doğru olduğundan emin olun.")
    st.stop()

# --- 2. MODELİ EĞİT ---
try:
    df = pd.read_csv(file_path)
    
    # Gereksiz sütun temizliği
    if 'Sample' in df.columns:
        df = df.drop(columns=['Sample'])
        
    X = df.drop(columns=['Cancer'])
    y = df['Cancer']
    
    # Modeli Taze Eğit
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)
    
except Exception as e:
    st.error(f"Veri okunurken veya model eğitilirken hata oluştu: {e}")
    st.stop()

# --- 3. KULLANICI GİRİŞİ ---
st.sidebar.header("Patient Metabolic Profile")

def user_input_features():
    # Slider değerleri
    gly = st.sidebar.slider('Glycolysis Score', 0.0, 15.0, 8.5)
    lip = st.sidebar.slider('Lipid Synthesis Score', 0.0, 15.0, 7.2)
    nuc = st.sidebar.slider('Nucleotide Metab. Score', 0.0, 15.0, 6.1)
    tca = st.sidebar.slider('TCA Cycle Score', 0.0, 15.0, 9.4)
    
    data = {'Glikoliz': gly, 'Lipid_Sentezi': lip, 'Nukleotit': nuc, 'TCA_Dongusu': tca}
    return pd.DataFrame(data, index=[0])

input_df = user_input_features()

# --- 4. TAHMİN BUTONU ---
st.divider()
st.subheader("Analiz Sonucu")

if st.button("🔍 Analyze"):
    try:
        # Tahmin
        prediction = model.predict(input_df)[0]
        # Olasılık
        prediction_proba = model.predict_proba(input_df)
        
        # Sonucu Yazdır
        if prediction == "PAAD":
            st.error(f"Tahmin: **{prediction}** (Pankreas Kanseri)")
            st.write("⚠️ Yüksek Riskli Agresif Profil")
        elif prediction == "OV":
            st.warning(f"Tahmin: **{prediction}** (Over Kanseri)")
            st.write("ℹ️ Yüksek Nükleotit Aktivitesi")
        else:
            st.success(f"Tahmin: **{prediction}** (Safra Yolu Kanseri)")
            st.write("✅ Düşük Metabolik Sinyal")
            
        # Grafik
        st.write("Güven Skorları:")
        st.bar_chart(pd.DataFrame(prediction_proba, columns=model.classes_).T)
        
    except Exception as e:
        st.error(f"Bir hata oluştu: {e}")
