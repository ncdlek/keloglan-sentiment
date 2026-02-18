"""
Keloğlan Unified Trainer
Handles both full training and fine-tuning in a single class.
"""

import pandas as pd
import torch
import os
import time
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    TrainingArguments,
    Trainer,
    DataCollatorWithPadding,
    EarlyStoppingCallback
)
from datasets import Dataset, load_from_disk, Value
from sklearn.metrics import accuracy_score, precision_recall_fscore_support
from ..utils import constants


class KeloTrainer:
    """
    Unified trainer for Keloğlan sentiment model.
    
    Supports two modes:
      - train():    Full training from base model on the global dataset
      - finetune(): Fine-tuning an existing model on a specific dataset
    """

    def __init__(self, model_name=None, output_dir=None):
        self.model_name = model_name or constants.BASE_MODEL
        self.output_dir = output_dir or constants.MODEL_DIR
        self.device = "mps" if torch.backends.mps.is_available() else "cpu"
        print(f"🍏 Device: {self.device.upper()}")

    @staticmethod
    def compute_metrics(pred):
        labels = pred.label_ids
        preds = pred.predictions.argmax(-1)
        precision, recall, f1, _ = precision_recall_fscore_support(
            labels, preds, average='weighted'
        )
        acc = accuracy_score(labels, preds)
        return {'accuracy': acc, 'f1': f1, 'precision': precision, 'recall': recall}

    def _load_tokenizer(self, model_path):
        """Load tokenizer from a model path."""
        return AutoTokenizer.from_pretrained(model_path, use_fast=True)

    def _load_model(self, model_path):
        """Load model with 3-class sentiment configuration."""
        model = AutoModelForSequenceClassification.from_pretrained(
            model_path,
            num_labels=3,
            id2label=constants.LABEL_MAP,
            label2id=constants.REVERSE_LABEL_MAP
        )
        model.to(self.device)
        return model

    def _prepare_label_map(self):
        """Return a label mapping function for string→int conversion."""
        label_map = constants.STRING_LABEL_MAP

        def map_label(example):
            l = example['label']
            if isinstance(l, str):
                return {'label': label_map.get(str(l).strip(), 1)}
            return {'label': int(l)}
        return map_label

    # =========================================================================
    # FULL TRAINING
    # =========================================================================
    def train(self, epochs=None, batch_size=None, custom_data_path=None):
        """
        Full training from the base model on the global dataset.
        
        Looks for pre-processed data first (Arrow format), falls back to CSV.
        """
        epochs = epochs or constants.EPOCHS
        batch_size = batch_size or constants.BATCH_SIZE

        print(f"🚀 Full Training Started")
        print(f"   Base Model : {self.model_name}")
        print(f"   Output     : {self.output_dir}")
        print(f"   Epochs     : {epochs}")
        print(f"   Batch Size : {batch_size} (effective: {batch_size * constants.GRAD_ACCUMULATION_STEPS})")

        # --- Data Loading ---
        if custom_data_path:
            print(f"🧪 Training on Custom Dataset: {custom_data_path}")
            tokenized_datasets, tokenizer = self._load_and_tokenize_csv(custom_data_path)
            if tokenized_datasets is None:
                return

        elif os.path.exists(constants.PROCESSED_DATA_DIR):
            print(f"⚡ Loading pre-processed dataset from {constants.PROCESSED_DATA_DIR}...")
            tokenized_datasets = load_from_disk(constants.PROCESSED_DATA_DIR)
            tokenizer = self._load_tokenizer(self.model_name)
        else:
            print("📖 Pre-processed data not found, loading from CSV...")
            tokenized_datasets, tokenizer = self._load_and_tokenize_csv()
            if tokenized_datasets is None:
                return

        # --- Model ---
        model = self._load_model(self.model_name)

        # --- Training Args ---
        total_steps = (len(tokenized_datasets["train"]) // (batch_size * constants.GRAD_ACCUMULATION_STEPS)) * epochs
        eval_steps = max(500, total_steps // 20)

        training_args = TrainingArguments(
            output_dir=self.output_dir,
            eval_strategy="steps",
            eval_steps=eval_steps,
            save_strategy="steps",
            save_steps=eval_steps,
            logging_steps=100,
            learning_rate=constants.LEARNING_RATE,
            per_device_train_batch_size=batch_size,
            per_device_eval_batch_size=batch_size * 2,
            gradient_accumulation_steps=constants.GRAD_ACCUMULATION_STEPS,
            num_train_epochs=epochs,
            weight_decay=constants.WEIGHT_DECAY,
            load_best_model_at_end=True,
            metric_for_best_model="f1",
            greater_is_better=True,
            save_total_limit=1,
            dataloader_num_workers=2,
            report_to="none",
            fp16=False,
            seed=constants.RANDOM_SEED,
            use_mps_device=(self.device == "mps")
        )

        trainer = Trainer(
            model=model,
            args=training_args,
            train_dataset=tokenized_datasets["train"],
            eval_dataset=tokenized_datasets["validation"],
            tokenizer=tokenizer,
            data_collator=DataCollatorWithPadding(tokenizer=tokenizer),
            compute_metrics=self.compute_metrics,
            callbacks=[EarlyStoppingCallback(
                early_stopping_patience=constants.EARLY_STOPPING_PATIENCE
            )]
        )

        # --- Execute ---
        start_time = time.time()
        trainer.train()
        elapsed = (time.time() - start_time) / 60

        # --- Save ---
        trainer.save_model(self.output_dir)
        tokenizer.save_pretrained(self.output_dir)

        # --- Final eval ---
        metrics = trainer.evaluate()
        print(f"\n⏱️  Training took {elapsed:.2f} minutes")
        print(f"📊 Final Eval: {metrics}")
        print(f"✅ Model saved to {self.output_dir}")

    # =========================================================================
    # FINE-TUNING
    # =========================================================================
    def finetune(self, data_path, sample_n=None, replay_n=10000,
                 epochs=None, batch_size=16, learning_rate=None):
        """
        Fine-tune an existing model on a specific dataset.
        
        Args:
            data_path:      Path to the fine-tuning CSV (must have 'text' and 'label' columns)
            sample_n:       Number of samples to take from fine-tune data (None = use all)
            replay_n:       Number of replay samples from global dataset to prevent forgetting
            epochs:         Number of fine-tuning epochs
            batch_size:     Per-device batch size
            learning_rate:  Learning rate (defaults to FINETUNE_LEARNING_RATE)
        """
        epochs = epochs or constants.FINETUNE_EPOCHS
        learning_rate = learning_rate or constants.FINETUNE_LEARNING_RATE

        # Use existing model as base
        base_model_path = self.output_dir
        if not os.path.exists(base_model_path):
            print(f"❌ Base model not found at {base_model_path}. Train first!")
            return

        print(f"🎯 Fine-Tuning Started")
        print(f"   Base Model : {base_model_path}")
        print(f"   Data       : {data_path}")
        print(f"   Epochs     : {epochs}")
        print(f"   LR         : {learning_rate}")

        # --- Load fine-tune data ---
        if not os.path.exists(data_path):
            print(f"❌ Data not found: {data_path}")
            return

        df_target = pd.read_csv(data_path)
        if sample_n and len(df_target) > sample_n:
            df_target = df_target.sample(n=sample_n, random_state=constants.RANDOM_SEED)
        print(f"   Target samples: {len(df_target)}")

        # --- Replay data (prevents catastrophic forgetting) ---
        if replay_n and os.path.exists(constants.TRAIN_DATASET):
            df_replay = pd.read_csv(constants.TRAIN_DATASET).sample(
                n=min(replay_n, 50000), random_state=constants.RANDOM_SEED
            )
            df_final = pd.concat([df_target, df_replay], ignore_index=True)
            df_final = df_final.sample(frac=1, random_state=constants.RANDOM_SEED).reset_index(drop=True)
            print(f"   Replay samples: {len(df_replay)}")
        else:
            df_final = df_target

        print(f"   Total training: {len(df_final)}")

        # --- Tokenize ---
        tokenizer = self._load_tokenizer(base_model_path)
        model = self._load_model(base_model_path)

        dataset = Dataset.from_pandas(df_final)
        dataset = dataset.map(self._prepare_label_map())

        def tokenize_fn(examples):
            return tokenizer(
                examples["text"], padding="max_length",
                truncation=True, max_length=constants.MAX_LEN
            )

        tokenized = dataset.map(tokenize_fn, batched=True)

        # Clean columns
        keep_cols = {'input_ids', 'attention_mask', 'label'}
        remove_cols = [c for c in tokenized.column_names if c not in keep_cols]
        tokenized = tokenized.remove_columns(remove_cols)
        tokenized = tokenized.cast_column("label", Value("int64"))

        # --- Training Args ---
        training_args = TrainingArguments(
            output_dir=self.output_dir,
            num_train_epochs=epochs,
            per_device_train_batch_size=batch_size,
            gradient_accumulation_steps=2,
            learning_rate=learning_rate,
            weight_decay=constants.WEIGHT_DECAY,
            logging_steps=100,
            save_strategy="no",
            report_to="none",
            seed=constants.RANDOM_SEED,
            use_mps_device=(self.device == "mps")
        )

        trainer = Trainer(
            model=model,
            args=training_args,
            train_dataset=tokenized,
            tokenizer=tokenizer,
            data_collator=DataCollatorWithPadding(tokenizer=tokenizer)
        )

        start_time = time.time()
        trainer.train()
        elapsed = (time.time() - start_time) / 60

        trainer.save_model(self.output_dir)
        tokenizer.save_pretrained(self.output_dir)

        print(f"\n⏱️  Fine-tuning took {elapsed:.2f} minutes")
        print(f"✅ Model saved to {self.output_dir}")

    # =========================================================================
    # HELPERS
    # =========================================================================
    def _load_and_tokenize_csv(self, override_path=None):
        """Load CSV dataset and tokenize on-the-fly (fallback when no pre-processed data)."""
        train_path = override_path or constants.TRAIN_DATASET
        val_path = constants.VAL_DATASET

        if not os.path.exists(train_path):
            print(f"❌ Training data not found: {train_path}")
            print("   Run 'python main.py build' first.")
            return None, None

        print(f"📖 Loading {train_path}...")
        df_train = pd.read_csv(train_path).dropna(subset=['text', 'label'])
        df_train['label'] = df_train['label'].astype(int)

        if os.path.exists(val_path):
            df_val = pd.read_csv(val_path).dropna(subset=['text', 'label'])
            df_val['label'] = df_val['label'].astype(int)
        else:
            # Auto-split if no separate val file
            split_idx = int(len(df_train) * (1 - constants.VAL_SPLIT))
            df_val = df_train.iloc[split_idx:]
            df_train = df_train.iloc[:split_idx]

        print(f"   Train: {len(df_train)}, Val: {len(df_val)}")

        tokenizer = self._load_tokenizer(self.model_name)

        def tokenize_fn(examples):
            return tokenizer(
                examples["text"], padding="max_length",
                truncation=True, max_length=constants.MAX_LEN
            )

        train_ds = Dataset.from_pandas(df_train).map(tokenize_fn, batched=True)
        val_ds = Dataset.from_pandas(df_val).map(tokenize_fn, batched=True)

        from datasets import DatasetDict
        tokenized_datasets = DatasetDict({"train": train_ds, "validation": val_ds})

        return tokenized_datasets, tokenizer
