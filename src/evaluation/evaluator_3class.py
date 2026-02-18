"""
3-Class Evaluator — evaluates sentiment models with detailed metrics.
"""

import torch
import numpy as np
import pandas as pd
import time
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from sklearn.metrics import accuracy_score, f1_score, classification_report, confusion_matrix
from tqdm import tqdm
from ..utils import constants


class Evaluator3Class:
    def __init__(self, model_path=None):
        self.model_path = model_path or constants.MODEL_DIR
        self.device = torch.device("mps") if torch.backends.mps.is_available() else torch.device("cpu")
        self.model = None
        self.tokenizer = None

    def load_model(self):
        if self.model is None:
            print(f"Loading model: {self.model_path}")
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_path)
            self.model = AutoModelForSequenceClassification.from_pretrained(self.model_path)
            self.model.to(self.device)
            print(f"Device: {self.device}")

    def predict(self, text):
        """Single text prediction."""
        self.load_model()
        inputs = self.tokenizer(
            text, return_tensors="pt", truncation=True,
            max_length=constants.MAX_LEN, padding=True
        ).to(self.device)

        with torch.no_grad():
            outputs = self.model(**inputs)

        probs = torch.nn.functional.softmax(outputs.logits, dim=-1)
        score = torch.argmax(probs).item()
        confidence = probs[0][score].item()
        label = constants.LABEL_MAP.get(score, "Unknown")
        return label, confidence, score

    def predict_batch(self, texts, batch_size=None):
        """Batch prediction for efficiency."""
        batch_size = batch_size or constants.INFERENCE_BATCH_SIZE
        self.load_model()

        all_predictions = []
        all_confidences = []

        for i in tqdm(range(0, len(texts), batch_size), desc="Inference"):
            batch = texts[i:i + batch_size]
            inputs = self.tokenizer(
                batch, return_tensors="pt", truncation=True,
                max_length=constants.MAX_LEN, padding=True
            ).to(self.device)

            with torch.no_grad():
                outputs = self.model(**inputs)

            probs = torch.nn.functional.softmax(outputs.logits, dim=-1)
            scores = torch.argmax(probs, dim=-1).cpu().numpy()
            confidences = probs.max(dim=-1)[0].cpu().numpy()

            all_predictions.extend(scores)
            all_confidences.extend(confidences)

        return np.array(all_predictions), np.array(all_confidences)

    def evaluate(self, csv_path=None, batch_size=None):
        """
        Evaluate model on a 3-class benchmark CSV.
        Returns dict with accuracy, F1, confusion matrix, etc.
        """
        csv_path = csv_path or constants.KELOGLAN_BENCHMARK
        batch_size = batch_size or constants.INFERENCE_BATCH_SIZE

        print(f"{'=' * 80}")
        print(f"3-CLASS EVALUATION")
        print(f"{'=' * 80}")
        print(f"Model: {self.model_path}")
        print(f"Data:  {csv_path}")

        try:
            df = pd.read_csv(csv_path)
        except Exception as e:
            print(f"❌ Cannot read: {e}")
            return None

        if 'label' not in df.columns or 'text' not in df.columns:
            print("❌ CSV must have 'text' and 'label' columns")
            return None

        df['label'] = df['label'].apply(lambda x: int(float(x)) if pd.notna(x) else 1)
        df = df.dropna(subset=['label', 'text'])

        print(f"\nSamples: {len(df)}")
        print(f"Distribution:\n{df['label'].value_counts().sort_index()}")

        # Inference
        start = time.time()
        predictions, confidences = self.predict_batch(
            df['text'].astype(str).tolist(), batch_size
        )
        elapsed = time.time() - start

        true_labels = df['label'].values
        acc = accuracy_score(true_labels, predictions)
        f1_m = f1_score(true_labels, predictions, average='macro')
        f1_w = f1_score(true_labels, predictions, average='weighted')

        report = classification_report(
            true_labels, predictions,
            labels=[0, 1, 2],
            target_names=[constants.LABEL_MAP[i] for i in [0, 1, 2]],
            output_dict=True,
            zero_division=0
        )
        cm = confusion_matrix(true_labels, predictions, labels=[0, 1, 2])


        # Print
        print(f"\n{'─' * 80}")
        print(f"Accuracy:    {acc:.4f} ({acc * 100:.2f}%)")
        print(f"F1 (Macro):  {f1_m:.4f}")
        print(f"F1 (Weight): {f1_w:.4f}")
        print(f"Speed:       {len(df) / elapsed:.0f} samples/sec")
        print(f"{'─' * 80}")

        for i in [0, 1, 2]:
            lbl = constants.LABEL_MAP[i]
            print(f"{lbl}: P={report[lbl]['precision']:.3f} R={report[lbl]['recall']:.3f} F1={report[lbl]['f1-score']:.3f}")

        print(f"\nConfusion Matrix:")
        print(f"         Neg  Neut  Pos")
        for i, name in enumerate(["Neg ", "Neut", "Pos "]):
            print(f"  {name}  {cm[i, 0]:>4}  {cm[i, 1]:>4}  {cm[i, 2]:>4}")
        print(f"{'=' * 80}\n")

        return {
            'accuracy': acc, 'f1_macro': f1_m, 'f1_weighted': f1_w,
            'confusion_matrix': cm.tolist(),
            'classification_report': report,
            'predictions': predictions.tolist(),
            'confidences': confidences.tolist()
        }
