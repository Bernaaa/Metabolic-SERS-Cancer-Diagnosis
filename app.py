import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import os

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="AI-SERS Cancer Diagnosis", page_icon="🧬")

# --- BAŞLIK ---
st.title("🧬 AI-Based Metabolic Cancer Diagnosis")

# --- 1. VERİYİ OKU, MODELİ EĞİT VE SÜTUN SIRASINI AL ---
@st.cache_resource
def train_model_live():
    file_name = "metabolic_scores_final.csv"
    
    # Dosya kontrolü (Klasörleri tara)
    file_path = None
    for root, dirs, files in os.walk("."):
        if file_name in files:
            file_path = os.path.join(root, file_name)
            break
            
    if file_path is None:
        return None, None, f"HATA: '{file_name}' dosyası bulunamadı. Lütfen GitHub'da dosyanın yüklü olduğundan emin olun."
    
    try:
        df = pd.read_csv(file_path)
        
        # Gereksiz sütun temizliği
        if 'Sample' in df.columns:
            df = df.drop(columns=['Sample'])
            
        X = df.drop(columns=['Cancer'])
        y = df['Cancer']
        
        # Sütun isimlerini kaydet (Sıralama hatasını önlemek için)
        feature_order = X.columns.tolist()
        
        # Modeli Eğit
        clf = RandomForestClassifier(n_estimators=100, random_state=42)
        clf.fit(X, y)
        
        return clf, feature_order, None
    except Exception as e:
        return None, None, str(e)

# Modeli ve Sütun Sırasını Yükle
model, feature_order, error = train_model_live()

# --- 2. HATA VARSA GÖSTER ---
if error:
    st.error(error)
    st.stop()

# --- 3. KULLANICI GİRİŞİ ---
st.sidebar.header("Patient Metabolic Profile")

def user_input_features():
    # Slider değerleri
    gly = st.sidebar.slider('Glikoliz', 0.0, 15.0, 8.5)
    lip = st.sidebar.slider('Lipid_Sentezi', 0.0, 15.0, 7.2)
    nuc = st.sidebar.slider('Nukleotit', 0.0, 15.0, 6.1)
    tca = st.sidebar.slider('TCA_Dongusu', 0.0, 15.0, 9.4)
    
    # Veriyi sözlük olarak oluştur
    data = {
        'Glikoliz': gly, 
        'Lipid_Sentezi': lip, 
        'Nukleotit': nuc, 
        'TCA_Dongusu': tca
    }
    
    # DataFrame oluştur
    features_df = pd.DataFrame(data, index=[0])
    
    # KRİTİK DÜZELTME: Sütunları, eğitimdeki sıraya göre yeniden diz
    # Bu satır "Feature names must be in the same order" hatasını çözer.
    features_df = features_df[feature_order]
    
    return features_df

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
