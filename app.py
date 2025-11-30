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
    # Dosya adını belirtiyoruz
    target_file = "metabolic_scores_final.csv"
    file_path = None

    # 1. Dosyayı Dinamik Olarak Ara (Current Directory ve Alt Klasörler)
    # Bu döngü, dosya nerede saklanıyorsa onu bulur.
    for root, dirs, files in os.walk("."):
        if target_file in files:
            file_path = os.path.join(root, target_file)
            break
            
    # 2. Dosya Bulunamadıysa Hata Ver
    if file_path is None:
        st.error(f"❌ KRİTİK HATA: '{target_file}' dosyası sunucuda bulunamadı!")
        st.info("Lütfen GitHub reponuzda bu dosyanın yüklü olduğundan emin olun.")
        st.write("Mevcut Klasördeki Dosyalar:", os.listdir(".")) # Debug için dosya listesi
        return None, None

    try:
        # 3. Dosyayı Oku
        df = pd.read_csv(file_path)
        
        # Gereksiz sütun temizliği
        if 'Sample' in df.columns:
            df = df.drop(columns=['Sample'])
            
        X = df.drop(columns=['Cancer'])
        y = df['Cancer']
        
        # 4. Modeli Eğit (Anlık Eğitim)
        model = RandomForestClassifier(n_estimators=200, random_state=42)
        model.fit(X, y)
        
        return model, file_path # Başarılı dönüş
        
    except Exception as e:
        return None, f"Veri okunurken hata oluştu: {e}"

# Modeli Yükle
model_result, error_message = get_model_and_data()

# --- BAŞLIK ---
st.title("🧬 AI-Based Metabolic Cancer Diagnosis")

# --- DURUM KONTROLÜ ---
if isinstance(model_result, tuple): # Hata döndüyse
    st.error(error_message)
elif model_result is None: # Dosya bulunamadıysa
    st.stop()
else:
    # Model başarıyla yüklendi
    model = model_result
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
