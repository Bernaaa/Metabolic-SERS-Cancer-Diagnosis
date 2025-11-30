#  Veri Seti Açıklaması (Data Dictionary)

Bu klasör, proje kapsamında kullanılan işlenmiş veri setlerini içerir.

###  `metabolic_scores_final.csv`
Bu dosya, makine öğrenmesi modelinin eğitilmesi için kullanılan ana veri setidir. 

* **Kaynak:** TCGA (The Cancer Genome Atlas) veritabanından alınan 656 hastanın RNA-Seq verileri.
* **İşlem:** Ham gen sayımları R (DESeq2/Limma) kullanılarak normalize edilmiş ve 4 ana metabolik yolağa ait aktivite skorlarına dönüştürülmüştür.

#### Sütun Açıklamaları:
| Sütun Adı | Açıklama |
| :--- | :--- |
| **Cancer** | Hedef değişken. Kanser Türü (PAAD, OV, CHOL). |
| **Glikoliz** | Tümörün glikolitik aktivite skoru (Laktat üretimi). |
| **Lipid_Sentezi** | Yağ asidi sentez yolağı aktivite skoru. |
| **Nukleotit** | DNA/RNA sentez hızı ve hücre çoğalma skoru. |
| **TCA_Dongusu** | Mitokondriyal enerji döngüsü aktivitesi. |
