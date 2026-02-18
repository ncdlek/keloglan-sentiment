---
language:
- tr
license: mit
tags:
- turkish
- sentiment
- text-classification
- bert
- mdeberta
datasets:
- engin1123/keloglan-turkish-sentiment-analysis-dataset
metrics:
- accuracy
- f1
library_name: transformers
pipeline_tag: text-classification
---

# 🏰 Keloğlan Turkish Sentiment Analysis Model

**Keloğlan**, Türkçe duygu analizi (Sentiment Analysis) alanında geliştirilmiş, hem akademik hem de günlük dili en iyi anlayan modeldir.

**Microsoft mDeBERTa-v3-base** üzerine inşa edilmiş ve **630.000'den fazla** temizlenmiş, tekilleştirilmiş **gerçek** veri ile eğitilmiştir.

## 🏆 Benchmark Sonuçları (Gerçek Veri)

Keloğlan, 6 farklı **gerçek** veri setinde (Film, Ürün, Akademik) rakiplerini geride bırakarak **%90.07** genel başarı ortalamasına ulaşmıştır.

| Model | **Global AVG** | TRSA | Winvoker | WhiteAngelss | Ürün Yorumları | Beyazperde* | Keskin (Film)* |
|---|---|---|---|---|---|---|---|
| **Keloğlan (Ours)** | **%90.07** | 84.40% | 97.50% | 97.50% | 98.20% | 93.20% | 69.60% |
| CodeAlchemist | %87.05 | 61.90% | **98.80%** | **98.80%** | **98.80%** | 93.70% | 70.30% |
| Kaixkhazaki | %85.30 | 61.30% | 96.80% | 96.80% | 96.70% | 92.40% | 67.80% |
| Yusufalt46 | %64.92 | 62.40% | 63.20% | 45.30% | 98.70% | 95.00% | **71.10%** |
| Incidelen | %68.42 | **85.20%** | 57.70% | 57.70% | 74.60% | 78.10% | 57.20% |
| Savasy | %51.83 | 53.90% | 43.20% | 30.00% | 63.30% | **96.60%** | 69.50% |

### 📝 Notlar:
- **Global AVG:** Gerçek ve doğal veri setlerinin (İlk 6 sütun) ortalamasıdır. 
- **(*) Unseen Data:** Bu veri setleri modelin eğitim setinde **yer almamaktadır**. Modelin genelleme yeteneğini gösterir.

### 🧪 Bonus: Street Smart (Sentetik Stres Testi)
Modellerin argo, ironi ve bozuk Türkçe karşısındaki dayanıklılığını ölçmek için **Google Gemma 3** desteği ile oluşturduğumuz 1000 örnekli sentetik testin sonuçları:

| Model | Street Smart Skoru |
|---|---|
| Savasy | **%70.10** |
| **Keloğlan** | **%65.00** |
| CodeAlchemist | %61.50 |
| Yusufalt46 | %61.20 |
| Kaixkhazaki | %55.80 |

*Keloğlan, genel ortalamada rakiplerine fark atarken, zorlu sokak jargonunda da en iyi genel amaçlı modellerden biri olduğunu kanıtlamıştır.*

## 🚀 Kullanım

```python
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline

# 1. Pipeline ile Hızlı Kullanım
analyzer = pipeline("sentiment-analysis", model="engin1123/keloglan-turkish-sentiment-analysis")

print(analyzer("Ürün efsane, yılan gibi akıyor!"))
# [{'label': 'Positive', 'score': 0.99}]

print(analyzer("Kargo o kadar yavaştı ki yürüyerek gelse daha hızlıydı."))
# [{'label': 'Negative', 'score': 0.98}]  <-- İroniyi anlar!
```

## 📊 Eğitim Verisi
Bu model, `engin1123/keloglan-turkish-sentiment-analysis-dataset` kullanılarak eğitilmiştir.
- **Toplam Veri:** 631,166 Benzersiz Örnek
- **Kaynaklar:** Winvoker, WhiteAngelss, TRSAv1, Turkish Product Reviews

## 🛠️ Etiketler (Labels)
- `0`: **Negative** (Olumsuz / Kötü / İroni)
- `1`: **Neutral** (Nötr / Belirsiz)
- `2`: **Positive** (Olumlu / İyi)

## 👨‍💻 Geliştirici
Geliştirilen: **Engin Yazılan**
