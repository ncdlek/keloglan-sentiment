# 🧙‍♂️ Keloğlan: Turkish Global Sentiment Analysis

**Keloğlan** is a state-of-the-art Turkish sentiment analysis model designed to handle the complexities of real-world language. Unlike standard models that only understand literal meanings, Keloğlan is **"Street Smart"**—it masters irony, sarcasm, slang, and cultural nuances.

![License](https://img.shields.org/badge/license-MIT-blue)
![Python](https://img.shields.org/badge/python-3.10%2B-green)
![HuggingFace](https://img.shields.org/badge/HuggingFace-Model-orange)

---

## 🌟 Why Keloğlan?

Standard NLP models (e.g., vanilla BERT or translation-based models) are typically trained on formal language. However, real-world Turkish on social media and e-commerce platforms is full of nuance:

*   *"Great (!) service indeed."* (Irony -> **Negative**)
*   *"Silivri is cold right now."* (Cultural Reference -> **Negative/Political**)
*   *"They ghosted me."* (Gen-Z Slang -> **Negative**)

**Keloğlan** is trained on the massive, 637,000+ sample [Keloğlan Global Sentiment Dataset](https://huggingface.co/datasets/engin1123/keloglan-global-sentiment-dataset), which blends high-quality social media data with supervised synthetic examples to capture these linguistic subtleties.

---

## 🏆 Performance (Ultimate Benchmark)

Keloğlan is the **Global Leader** in aggregate performance across varied Turkish linguistic environments, significantly outperforming competitors in social media and informal language contexts.

| Rank | Model | **Global AVG** | E-Commerce (TRSAv1) | Social Media (Winvoker) | Street Smart (Slang) |
|---|---|---|---|---|---|
| 🥇 | **Keloğlan (Ours)** | **69.83%** | 78.80% | **95.40%** | **83.33%** |
| 🥈 | Incidelen (XLM-R) | 67.26% | **85.20%** | 57.70% | 73.15% |
| 🥉 | Gorengoz (Winvoker)| 60.72% | 50.70% | 61.50% | 66.67% |

---

## 🚀 Installation

Clone the repository and install the requirements in a clean environment:

```bash
git clone https://github.com/engin1123/keloglan-sentiment.git
cd keloglan-sentiment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## 🛠️ Usage (CLI)

The project features a unified command-line interface (`main.py`) to manage the entire pipeline.

### 1. Build the Dataset (`build`)
Fetch, clean, and merge data from Hugging Face and local sources.
```bash
python main.py build
```
*Output:* `data/keloglan_global_sentiment_dataset.csv` (~637k samples)

### 2. Train the Model (`train`)
Train the model from scratch or fine-tune existing versions.
```bash
python main.py train --epochs 2 --batch 16
```
*Output:* `models/keloglan-turkish-sentiment-v4`

### 3. Run Benchmark (`benchmark`)
Compete against top Turkish models (Incidelen, Savasy, etc.) across 4 distinct arenas.
```bash
python main.py benchmark
```
*Output:* `ULTIMATE_BENCHMARK_REPORT.md`

---

## 📦 Python Inference

Use Keloğlan directly in your Python applications:

```python
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

model_name = "engin1123/keloglan-turkish-v3-sota" # Hugging Face Model ID
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)

text = "Bu fiyata bedava resmen!"
inputs = tokenizer(text, return_tensors="pt")
outputs = model(**inputs)
probs = torch.softmax(outputs.logits, dim=-1)
label_id = torch.argmax(probs).item()

# 0: Negative, 1: Neutral, 2: Positive
labels = {0: "Negative", 1: "Neutral", 2: "Positive"}
print(f"Sentiment: {labels[label_id]}")
# Output: Positive
```

---

## 📜 License

This project is licensed under the **MIT License**. Please also adhere to the specific licenses of the source datasets (Winvoker, TRSAv1, etc.).

---
*Developed by Engin Yazılan.*
