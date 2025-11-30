import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="AI-SERS Cancer Diagnosis", page_icon="🧬", layout="centered")

# --- BAŞLIK ---
st.title("🧬 AI-Based Metabolic Cancer Diagnosis")
st.markdown("""
Bu uygulama, **Transkriptomik Rehberli SERS** verilerini kullanarak abdominal kanserlerin (PAAD, OV, CHOL) ayırıcı tanısını yapar.
Model, yüklenen veri seti üzerinde anlık olarak eğitilir ve **Olasılık Skorları (Probability Scores)** üretir.
""")

# --- 1. VERİYİ YÜKLEME VE MODEL EĞİTİMİ (CACHE) ---
# @st.cache_resource sayesinde model sadece bir kez eğitilir, her tıklamada tekrar etmez.
@st.cache_resource
def train_model():
    try:
        # GitHub'daki csv dosyasını okur
        df = pd.read_csv("metabolic_scores_final.csv")
        
        # Gereksiz sütun varsa temizle
        if 'Sample' in df.columns:
            df = df.drop(columns=['Sample'])
            
        X = df.drop(columns=['Cancer'])
        y = df['Cancer']
        
        # Modeli Eğit (Olasılık hesaplama özelliği varsayılan olarak açıktır)
        model = RandomForestClassifier(n_estimators=200, random_state=42)
        model.fit(X, y)
        
        return model, X.columns.tolist()
        
    except FileNotFoundError:
        st.error("HATA: 'metabolic_scores_final.csv' dosyası bulunamadı! Lütfen bu dosyayı GitHub reponuza yükleyin.")
        return None, None

# Modeli ve Sütun İsimlerini Al
model, feature_names = train_model()

st.divider()

if model:
    # --- 2. KULLANICI GİRİŞ PANELİ ---
    st.sidebar.header("Patient Metabolic Profile")
    st.sidebar.info("SERS sinyal yoğunluklarını giriniz.")

    # Slider'lar
    gly = st.sidebar.slider('Glycolysis Score (Lactate)', 0.0, 15.0, 8.5)
    lip = st.sidebar.slider('Lipid Synthesis Score', 0.0, 15.0, 7.2)
    nuc = st.sidebar.slider('Nucleotide Metab. Score', 0.0, 15.0, 6.1)
    tca = st.sidebar.slider('TCA Cycle Score', 0.0, 15.0, 9.4)
    
    # Giriş verisini DataFrame'e çevir
    # Sütun sırasının eğitim verisiyle aynı olduğundan emin oluyoruz
    input_data = {'Glikoliz': gly, 'Lipid_Sentezi': lip, 'Nukleotit': nuc, 'TCA_Dongusu': tca}
    input_df = pd.DataFrame([input_data])

    # --- 3. ANA EKRAN VE TAHMİN ---
    st.subheader("📊 Analiz Edilen Profil")
    st.dataframe(input_df)

    if st.button("🔍 Analyze & Diagnose"):
        # Tahmin (Sınıf)
        prediction = model.predict(input_df)[0]
        
        # Olasılık (Probability) - İsteğiniz üzerine eklendi
        prediction_proba = model.predict_proba(input_df)
        
        st.divider()
        
        # --- SONUÇ GÖSTERİMİ ---
        st.subheader("🩺 Tanı Sonucu")
        
        if prediction == "PAAD":
            st.error(f"Tahmin: **Pankreas Adenokarsinomu (PAAD)**")
            st.warning("⚠️ Yüksek Glikoliz ve Lipid Sentezi tespit edildi. Agresif seyir riski.")
        elif prediction == "OV":
            st.error(f"Tahmin: **Over Kanseri (OV)**")
            st.info("ℹ️ Yüksek Nükleotit sentezi tespit edildi. Hızlı proliferasyon işareti.")
        else:
            st.success(f"Tahmin: **Kolanjiyokarsinom (CHOL)**")
            st.info("ℹ️ Metabolik sinyaller düşük seviyede.")

        # --- OLASILIK GRAFİĞİ (Bar Chart) ---
        st.subheader("📈 Güven Skorları (Probability)")
        
        # Olasılıkları DataFrame'e çevirip çizdiriyoruz
        prob_df = pd.DataFrame(prediction_proba, columns=model.classes_)
        
        # En yüksek olasılığı yüzde olarak göster
        max_prob = np.max(prediction_proba) * 100
        st.write(f"Model bu karardan **%{max_prob:.2f}** oranında emin.")
        
        st.bar_chart(prob_df.T)

else:
    st.warning("Model eğitilemediği için arayüz yüklenemedi. Lütfen CSV dosyasını kontrol edin.")

# --- ALT BİLGİ ---
st.divider()
st.caption("Developed for ML Bootcamp Capstone Project")
