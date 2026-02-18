---
language:
- tr
license: cc-by-nc-4.0
task_categories:
- text-classification
tags:
- turkish
- sentiment
- reviews
- nlp
- large-scale
pretty_name: Keloğlan Turkish Sentiment Dataset (630k+)
size_categories:
- 100K<n<1M
---

# 🏰 Keloğlan Turkish Sentiment Analysis Dataset

This dataset represents one of the largest and most comprehensive sentiment analysis collections for the Turkish language, containing over **630,000 unique samples**. 

It was meticulously constructed by merging, cleaning, and deduplicating several major open-source Turkish sentiment datasets to train the **Keloğlan** model series.

## 📊 Dataset Statistics

- **Total Unique Samples:** 631,166
- **Training Set:** 599,607
- **Validation Set:** 31,559
- **Label Distribution:** 
    - `0` (Negative): Mixed sources (Reviews + Irony)
    - `1` (Neutral): Objective statements, mixed feelings
    - `2` (Positive): High satisfaction reviews

## 🧩 Data Sources & Construction

This dataset is a unification of the following sources, processed to create a standardized format:

1.  **WhiteAngelss/Turkce-Duygu-Analizi-Dataset:** E-commerce reviews (mapped 1-5 stars to Neg/Neu/Pos).
2.  **Winvoker/turkish-sentiment-analysis-dataset:** A large collection of movie and product reviews.
3.  **Maydogan/Turkish_SentimentAnalysis_TRSAv1:** A well-known benchmark dataset.
4.  **Turkish Product Reviews:** Additional diverse product feedback.

### 🛠️ Preprocessing Pipeline
To ensure high quality and prevent data leakage:
1.  **Standardization:** All labels were mapped to a unified `{0: Negative, 1: Neutral, 2: Positive}` schema.
2.  **Deduplication:** Aggressive deduplication was applied. From an initial pool of **1.26 million** rows, we removed exact text duplicates, resulting in **631k unique samples**. This prevents the model from memorizing repetitive comments (e.g., "Teşekkürler", "Kargo hızlıydı").
3.  **Cleaning:** Removed extremely short texts (len < 3) and noise.
4.  **Shuffling:** The dataset is fully shuffled to ensure balanced batches during training.

## 🚀 How to Use

```python
from datasets import load_dataset

# Load the full dataset
dataset = load_dataset("engin1123/keloglan-turkish-sentiment-analysis-dataset")

# Access splits
train_data = dataset['train']
val_data = dataset['validation']

print(train_data[0])
# Output: {'text': 'Ürün gayet başarılı...', 'label': 2}
```

## ⚖️ License
This dataset is a compilation of open-source datasets. Users should refer to the original licenses of the source datasets (Winvoker, WhiteAngelss, TRSAv1). The compilation itself is shared under **CC-BY-NC 4.0**.

## 👨‍💻 Maintainer
Maintained by **Engin Yazilan** for the **Keloğlan** project.
