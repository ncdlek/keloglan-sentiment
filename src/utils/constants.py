"""
Centralized constants for Keloğlan Sentiment Analysis
All configuration values should be defined here.
Templates and slang data live in templates.py.
"""

# ============================================================================
# MODEL PATHS
# ============================================================================
BASE_MODEL = "microsoft/mdeberta-v3-base"
MODEL_DIR = "models/keloglan-sentiment"

# ============================================================================
# DATA PATHS
# ============================================================================
DATA_DIR = "data"
RAW_DATA_DIR = "data/raw"
PROCESSED_DATA_DIR = "data/processed/processed_keloglan_dataset"
BENCHMARK_DATA_DIR = "data/benchmark"

# Dataset files (under data/final/)
TRAIN_DATASET = "data/final/keloglan_global_sentiment_dataset.csv"
VAL_DATASET = "data/final/keloglan_global_sentiment_val.csv"

# Benchmark files
KELOGLAN_BENCHMARK = "data/benchmark/keloglan_benchmark_100.csv"

# ============================================================================
# LABEL MAPPINGS
# ============================================================================
LABEL_MAP = {
    0: "Negative",
    1: "Neutral",
    2: "Positive"
}

REVERSE_LABEL_MAP = {
    "Negative": 0,
    "Neutral": 1,
    "Positive": 2
}

STRING_LABEL_MAP = {
    "Negative": 0, "Notr": 1, "Neutral": 1, "Positive": 2,
    "Pos": 2, "Neg": 0,
    "negative": 0, "neutral": 1, "positive": 2,
    "0": 0, "1": 1, "2": 2
}

BINARY_LABEL_MAP = {"True": 1, "False": 0}

BENCHMARK_LABEL_MAP = {
    "Olumlu": 2, "Olumsuz": 0,
    "Positive": 2, "Negative": 0
}

# ============================================================================
# TRAINING HYPERPARAMETERS
# ============================================================================
MAX_LEN = 128
BATCH_SIZE = 8
GRAD_ACCUMULATION_STEPS = 8  # Effective batch size = 64
LEARNING_RATE = 2e-5
EPOCHS = 3
WEIGHT_DECAY = 0.01
RANDOM_SEED = 42
VAL_SPLIT = 0.05
EARLY_STOPPING_PATIENCE = 3

# Fine-tuning defaults (lower LR, fewer epochs to prevent forgetting)
FINETUNE_LEARNING_RATE = 1e-5
FINETUNE_EPOCHS = 1

# ============================================================================
# SYNTHETIC DATA GENERATION
# ============================================================================
SYNTHETIC_COUNT = 20000
REAL_RATIO = 0.7

# Hard Example Mining Configuration
HARD_EXAMPLE_CONFIDENCE_THRESHOLD = 0.6  # Below this = uncertain
HARD_EXAMPLE_HIGH_CONFIDENCE = 0.7       # Above this + wrong = bad mistake
CURRICULUM_EASY_RATIO = 0.5              # 50% easy examples
CURRICULUM_MEDIUM_RATIO = 0.3            # 30% medium examples
CURRICULUM_HARD_RATIO = 0.2              # 20% hard examples

CATEGORY_WEIGHTS = {
    "fashion": 10, "cosmetic": 8, "tech": 10, "student": 10,
    "art": 8, "2ndhand": 5, "ks": 8, "neutral": 10,
    "irony": 15, "culture_neg": 15, "culture_pos": 20,
    "noise": 5, "gamer": 8, "rel": 8, "food": 6, "life": 5
}

# ============================================================================
# EVALUATION CONSTANTS
# ============================================================================
INFERENCE_BATCH_SIZE = 32
CONFIDENCE_THRESHOLD = 0.6

# ============================================================================
# BENCHMARK MODEL LIST
# ============================================================================
BENCHMARK_MODELS = {
    "Keloğlan": MODEL_DIR,
    "Savasy (BERT)": "savasy/bert-base-turkish-sentiment-cased",
    "Gorengoz (Winvoker)": "Gorengoz/bert-turkish-sentiment-analysis-winvoker",
    "TolgaDev (THY)": "tolgadev/TurkishAirlines-SentimentAnalysisModel",
    "Kaixkhazaki (BERT)": "kaixkhazaki/turkish-sentiment",
    "Saribasmetehan (BERT)": "saribasmetehan/bert-base-turkish-sentiment-analysis",
    "Incidelen (XLM-R)": "incidelen/xlm-roberta-base-turkish-sentiment-analysis",
    "Agentlans (E5-Small)": "agentlans/multilingual-e5-small-aligned-sentiment"
}

# ============================================================================
# HUGGING FACE HUB
# ============================================================================
HF_MODEL_REPO = "engin1123/keloglan-turkish-sentiment-analysis"
HF_DATASET_REPO = "engin1123/keloglan-turkish-sentiment-analysis-dataset"
