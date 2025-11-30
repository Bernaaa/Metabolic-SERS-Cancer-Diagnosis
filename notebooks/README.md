#  Analiz Not Defterleri (Notebooks)

Bu klasör, projenin Python tabanlı veri analizi ve modelleme süreçlerini içeren Jupyter Notebook dosyalarını barındırır. Analiz akışı aşağıdaki sırayla gerçekleştirilmiştir:

###  `1_EDA_and_Preprocessing.ipynb`
* **Amaç:** Keşifçi Veri Analizi (EDA).
* **İçerik:**
    * Veri setinin yüklenmesi ve kalite kontrolü.
    * Kanser türlerine göre metabolik skorların dağılımı (Boxplots).
    * Özellikler arası korelasyon analizi (Heatmap).

###  `2_Model_Training.ipynb`
* **Amaç:** Makine Öğrenmesi Modelinin Geliştirilmesi.
* **İçerik:**
    * Verinin Eğitim/Test (%70/%30) setlerine ayrılması (Stratified Split).
    * **Random Forest Classifier** modelinin eğitilmesi.
    * Model performansının değerlendirilmesi (Accuracy, Classification Report).
    * Eğitilen modelin (`.pkl`) kaydedilmesi.
