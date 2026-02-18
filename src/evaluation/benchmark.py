"""
Battle Arena Benchmark — compares Keloğlan against top Turkish sentiment models.
"""

import torch
import numpy as np
import pandas as pd
import time
import os
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from datasets import load_dataset
from sklearn.metrics import accuracy_score
from ..utils import constants

# ============================================================================
# CONFIGURATION
# ============================================================================
SAMPLE_SIZE = 1000
DEVICE = torch.device("mps") if torch.backends.mps.is_available() else torch.device("cpu")

MODELS = {
    "Keloğlan (Ours)": constants.MODEL_DIR,
    "Synthetic-Only (2k)": "models/keloglan-synthetic-v1",
    "Global SOTA (Twitter-XLM-R)": "cardiffnlp/twitter-xlm-roberta-base-sentiment",
    "Savasy (BERT)": "savasy/bert-base-turkish-sentiment-cased",
}

RAW = constants.RAW_DATA_DIR
BENCH = constants.BENCHMARK_DATA_DIR

# ============================================================================
# DATA LOADING
# ============================================================================
def _load_csv(path, text_col="text", label_col="label", label_map=None, sample=True):
    """Generic loader."""
    if not os.path.exists(path):
        print(f"    Not found: {path}")
        return pd.DataFrame()
    
    for encoding in ["utf-8", "iso-8859-9", "windows-1254", "latin1"]:
        try:
            df = pd.read_csv(path, encoding=encoding)
            break
        except UnicodeDecodeError:
            continue
    else:
        print(f"    ❌ Failed to decode: {path}")
        return pd.DataFrame()
    if text_col != "text":
        df = df.rename(columns={text_col: "text"})
    if label_col != "label":
        df = df.rename(columns={label_col: "label"})
    if label_map:
        df['label'] = df['label'].map(label_map)
    df = df.dropna(subset=['text', 'label'])
    if sample and len(df) > SAMPLE_SIZE:
        df = df.sample(n=SAMPLE_SIZE, random_state=42)
    return df


def load_trsa_3class():
    print("  Loading TRSAv1 (3-Class)...")
    return _load_csv(f"{RAW}/trsa_v1.csv", "review", "score",
                     {'Positive': 2, 'Neutral': 1, 'Negative': 0})

def load_winvoker_3class():
    print("  Loading Winvoker (3-Class)...")
    return _load_csv(f"{RAW}/winvoker_sentiment.csv", "text", "label",
                     {'Positive': 2, 'Notr': 1, 'Negative': 0})

def load_whiteangelss():
    print("  Loading WhiteAngelss (3-Class)...")
    return _load_csv(f"{RAW}/whiteangelss_sentiment.csv", "text", "label",
                     {'Positive': 2, 'Notr': 1, 'Negative': 0})

def load_keloglan_street():
    print("  Loading Keloğlan Street Smart...")
    return _load_csv(f"{BENCH}/keloglan_benchmark_100.csv", sample=False)

def load_turkish_product_reviews():
    print("  Loading Turkish Product Reviews...")
    return _load_csv(f"{RAW}/turkish_product_reviews.csv", "sentence", "sentiment",
                     {0: 0, 1: 2})

def load_fsmtsad():
    print("  Loading FSMTSAD (Balanced 3-Class)...")
    for path in [f"{RAW}/fsmtsa.csv", f"{constants.PROCESSED_DATA_DIR}/fsmtsa.csv"]:
        if os.path.exists(path):
            return _load_csv(path, "Sentence", "Label")
    print("    Not found")
    return pd.DataFrame()

def load_beyazperde():
    print("  Loading Beyazperde (Binary)...")
    for path in [f"{BENCH}/beyazperde_test.csv", f"{RAW}/beyazperde_test.csv"]:
        if os.path.exists(path):
            df = _load_csv(path, "comment", "Label", {0: 0, 1: 2})
            df['text'] = df['text'].astype(str).str.strip()
            return df
    return pd.DataFrame()

def load_laco_handlabelled():
    print("  Loading LACO Handlabelled (3-Class)...")
    df = _load_csv(f"{BENCH}/laco_handlabelled.csv", sample=False)
    if not df.empty and df['label'].dtype == object:
        df['label'] = df['label'].str.lower().map({'negative': 0, 'neutral': 1, 'positive': 2})
        df = df.dropna(subset=['label'])
    return df

def load_turkish_10k_sample():
    print("  Loading Sentetik Data (3-Class)...")
    return _load_csv(f"{BENCH}/turkish_10k_sample_1k.csv", sample=False)

def load_llm_synthetic():
    print("  Loading LLM Synthetic (Hard Examples)...")
    path = "data/synthetic/llm_generated_v1.csv"
    if os.path.exists(path):
        return _load_csv(path, sample=False)
    return pd.DataFrame()


# ============================================================================
# BATTLE ARENA
# ============================================================================
class BattleArena:
    def __init__(self):
        self.results = {}

    def predict(self, model, tokenizer, texts, return_probs=False):
        model.eval()
        preds, probs = [], []
        batch_size = 32

        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            inputs = tokenizer(batch, return_tensors="pt", padding=True,
                             truncation=True, max_length=128).to(DEVICE)
            with torch.no_grad():
                outputs = model(**inputs)
            batch_preds = torch.argmax(outputs.logits, dim=-1).cpu().numpy()
            preds.extend(batch_preds)
            if return_probs:
                batch_probs = torch.softmax(outputs.logits, dim=-1).cpu().numpy()
                probs.extend(batch_probs)

        if return_probs:
            return np.array(preds), np.array(probs)
        return np.array(preds)

    def run(self):
        print("\n📥 Preparing Battlegrounds...")
        datasets = {
            "TRSAv1 (3Cls)": load_trsa_3class(),
            #"Winvoker (3Cls)": load_winvoker_3class(),
            #"WhiteAngelss": load_whiteangelss(),
            #"FSMTSAD": load_fsmtsad(),
            #"LACO Handlabelled": load_laco_handlabelled(),
            #"Sentetik Data": load_turkish_10k_sample(),
            "LLM Synthetic (Hard)": load_llm_synthetic(),
            #"Product Reviews": load_turkish_product_reviews(),
            #"Beyazperde": load_beyazperde(),
        }
        datasets = {k: v for k, v in datasets.items() if not v.empty}
        print(f"✅ Ready with {len(datasets)} datasets.\n")

        print("⚔️  LET THE BATTLE BEGIN! ⚔️")

        final_scores = {m: {} for m in MODELS}
        model_num_labels = {}

        for model_name, model_path in MODELS.items():
            print(f"\n🤖 {model_name}")
            try:
                use_fast = "xlm-roberta" not in model_path
                tokenizer = AutoTokenizer.from_pretrained(model_path, use_fast=use_fast)
                model = AutoModelForSequenceClassification.from_pretrained(model_path).to(DEVICE)
            except Exception as e:
                print(f"   ❌ Load failed: {e}")
                continue

            num_labels = model.config.num_labels
            model_num_labels[model_name] = num_labels

            for ds_name, df in datasets.items():
                # Robust label conversion
                df = df.copy()
                df['label'] = pd.to_numeric(df['label'], errors='coerce')
                df = df.dropna(subset=['label'])
                if df.empty:
                    print(f"   ⚠️ Skipping {ds_name}: No valid numeric labels found.")
                    continue

                texts = df['text'].astype(str).tolist()
                true_labels = df['label'].astype(int).values
                is_binary = ds_name in ["Product Reviews", "Beyazperde"]

                if num_labels == 3 and not is_binary:
                    preds = self.predict(model, tokenizer, texts)
                    acc = accuracy_score(true_labels, preds)
                    final_scores[model_name][ds_name] = acc * 100
                    print(f"   {ds_name}: {acc * 100:.2f}%")

                elif num_labels == 2 and is_binary:
                    preds = self.predict(model, tokenizer, texts)
                    mapped = np.where(preds == 1, 2, 0)
                    acc = accuracy_score(true_labels, mapped)
                    final_scores[model_name][ds_name] = acc * 100
                    print(f"   {ds_name}: {acc * 100:.2f}%")

                elif num_labels == 3 and is_binary:
                    preds, probs = self.predict(model, tokenizer, texts, return_probs=True)
                    binary_preds = []
                    for j, p in enumerate(preds):
                        if p == 0:
                            binary_preds.append(0)
                        elif p == 2:
                            binary_preds.append(1)
                        else:
                            binary_preds.append(0 if probs[j][0] > probs[j][2] else 1)
                    mapped = np.where(np.array(binary_preds) == 1, 2, 0)
                    acc = accuracy_score(true_labels, mapped)
                    final_scores[model_name][ds_name] = acc * 100
                    print(f"   {ds_name}: {acc * 100:.2f}% (3→2 mapped)")

                elif num_labels == 2 and not is_binary:
                    preds = self.predict(model, tokenizer, texts)
                    mapped = np.where(preds == 1, 2, 0)
                    mask = true_labels != 1
                    if np.any(mask):
                        acc = accuracy_score(true_labels[mask], mapped[mask])
                        print(f"   {ds_name}: {acc * 100:.2f}%* (non-neutral only)")

        self._generate_report(final_scores, model_num_labels)

    def _generate_report(self, scores, model_num_labels):
        print("\n" + "=" * 100)
        print("🏆 BENCHMARK RESULTS")
        print("=" * 100)

        three_class_models = [m for m in scores if model_num_labels.get(m) == 3]
        three_class_ds = ["TRSAv1 (3Cls)", "Winvoker (3Cls)", "WhiteAngelss",
                          "FSMTSAD", "LACO Handlabelled", "Sentetik Data", "LLM Synthetic (Hard)"]
        binary_ds = ["Product Reviews", "Beyazperde"]

        # 3-class averages
        for m in three_class_models:
            vals = [scores[m].get(d, 0) for d in three_class_ds if scores[m].get(d, 0) > 0]
            scores[m]['AVG_3CLASS'] = sum(vals) / len(vals) if vals else 0

        sorted_3 = sorted(three_class_models, key=lambda m: scores[m]['AVG_3CLASS'], reverse=True)

        print(f"\n{'Rank':<6} {'Model':<25} {'AVG':>10}", end="")
        for d in three_class_ds:
            print(f" | {d:>12}", end="")
        print()
        print("-" * 120)

        rows_3 = []
        for rank, m in enumerate(sorted_3, 1):
            medal = ["🥇", "🥈", "🥉"][rank - 1] if rank <= 3 else f"{rank}."
            avg = scores[m]['AVG_3CLASS']
            row = [scores[m].get(d, 0) for d in three_class_ds]
            print(f"{medal:<6} {m:<25} {avg:>9.2f}%", end="")
            for v in row:
                print(f" | {v:>11.2f}%", end="")
            print()
            rows_3.append((medal, m, avg, *row))

        # Binary leaderboard
        two_class_models = [m for m in scores if model_num_labels.get(m) == 2]
        binary_models = two_class_models.copy()
        if scores.get("Keloğlan (Ours)", {}).get("Product Reviews", 0) > 0:
            binary_models.append("Keloğlan (Ours)")

        for m in binary_models:
            vals = [scores[m].get(d, 0) for d in binary_ds if scores[m].get(d, 0) > 0]
            scores[m]['AVG_BINARY'] = sum(vals) / len(vals) if vals else 0

        sorted_b = sorted(binary_models, key=lambda m: scores[m]['AVG_BINARY'], reverse=True)

        print(f"\n{'Rank':<6} {'Model':<25} {'AVG':>10} | {'Product Reviews':>15} | {'Beyazperde':>12}")
        print("-" * 80)

        rows_b = []
        for rank, m in enumerate(sorted_b, 1):
            medal = ["🥇", "🥈", "🥉"][rank - 1] if rank <= 3 else f"{rank}."
            avg = scores[m]['AVG_BINARY']
            d1 = scores[m].get("Product Reviews", 0)
            d2 = scores[m].get("Beyazperde", 0)
            note = " (3→2)" if m == "Keloğlan (Ours)" else ""
            print(f"{medal:<6} {m:<25} {avg:>9.2f}% | {d1:>14.2f}% | {d2:>11.2f}%{note}")
            rows_b.append((medal, m, avg, d1, d2, note))

        # Save report
        with open("ULTIMATE_BENCHMARK_REPORT.md", "w") as f:
            f.write("# Turkish Sentiment Analysis Benchmark\n\n")
            f.write(f"**Date:** {time.strftime('%Y-%m-%d')}\n\n")

            f.write("## 🥇 3-Class Leaderboard\n\n")
            f.write("| Rank | Model | **AVG** | " + " | ".join(three_class_ds) + " |\n")
            f.write("|:---:|---|---:" + "|---:" * len(three_class_ds) + "|\n")
            for r in rows_3:
                f.write(f"| {r[0]} | {r[1]} | **{r[2]:.2f}%** |")
                for v in r[3:]:
                    f.write(f" {v:.2f}% |")
                f.write("\n")

            f.write("\n## 🥈 Binary Leaderboard\n\n")
            f.write("| Rank | Model | **AVG** | Product Reviews | Beyazperde |\n")
            f.write("|:---:|---|---:|---:|---:|\n")
            for r in rows_b:
                note = r[5] if len(r) > 5 else ""
                f.write(f"| {r[0]} | {r[1]}{note} | **{r[2]:.2f}%** | {r[3]:.2f}% | {r[4]:.2f}% |\n")

        print("\n📄 Report saved to ULTIMATE_BENCHMARK_REPORT.md")


if __name__ == "__main__":
    arena = BattleArena()
    arena.run()
