import streamlit as st
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import os

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="AI-SERS Cancer Diagnosis", page_icon="🧬")

# --- BAŞLIK ---
st.title("🧬 AI-Based Metabolic Cancer Diagnosis")

# --- 1. VERİYİ OKU VE MODELİ EĞİT ---
# Bu fonksiyon modeli her seferinde sıfırdan eğitir, böylece versiyon hatası olmaz.
@st.cache_resource
def train_model_live():
    file_name = "metabolic_scores_final.csv"
    
    # Dosya kontrolü
    if not os.path.exists(file_name):
        return None, f"HATA: '{file_name}' dosyası bulunamadı. Lütfen GitHub'da dosya adının birebir aynı olduğundan emin olun."
    
    try:
        df = pd.read_csv(file_name)
        
        # Gereksiz sütun temizliği
        if 'Sample' in df.columns:
            df = df.drop(columns=['Sample'])
            
        X = df.drop(columns=['Cancer'])
        y = df['Cancer']
        
        # Modeli Eğit
        clf = RandomForestClassifier(n_estimators=100, random_state=42)
        clf.fit(X, y)
        
        return clf, None
    except Exception as e:
        return None, str(e)

# Modeli al
model, error = train_model_live()

# --- 2. HATA VARSA GÖSTER, YOKSA DEVAM ET ---
if error:
    st.error(error)
    st.write("Mevcut Klasördeki Dosyalar:", os.listdir()) # Hata ayıklama için
    st.stop()

# --- 3. KULLANICI GİRİŞİ ---
st.sidebar.header("Patient Metabolic Profile")

def user_input_features():
    gly = st.sidebar.slider('Glycolysis Score', 0.0, 15.0, 8.5)
    lip = st.sidebar.slider('Lipid Synthesis Score', 0.0, 15.0, 7.2)
    nuc = st.sidebar.slider('Nucleotide Metab. Score', 0.0, 15.0, 6.1)
    tca = st.sidebar.slider('TCA Cycle Score', 0.0, 15.0, 9.4)
    
    data = {'Glikoliz': gly, 'Lipid_Sentezi': lip, 'Nukleotit': nuc, 'TCA_Dongusu': tca}
    return pd.DataFrame(data, index=[0])

input_df = user_input_features()

# --- 4. TAHMİN ---
st.subheader("Analiz Sonucu")

if st.button("🔍 Analyze"):
    prediction = model.predict(input_df)[0]
    prediction_proba = model.predict_proba(input_df)
    
    if prediction == "PAAD":
        st.error(f"Tahmin: **{prediction}** (Pankreas Kanseri)")
    elif prediction == "OV":
        st.warning(f"Tahmin: **{prediction}** (Over Kanseri)")
    else:
        st.success(f"Tahmin: **{prediction}** (Safra Yolu Kanseri)")
        
    st.bar_chart(pd.DataFrame(prediction_proba, columns=model.classes_).T)
