# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Keloğlan** is a state-of-the-art Turkish sentiment analysis model that handles irony, sarcasm, slang, and cultural nuances ("Street Smart" capabilities). Unlike standard models trained only on formal language, Keloğlan excels on real-world Turkish text from social media and e-commerce platforms.

The model is trained on the ~637K sample Keloğlan Global Sentiment Dataset and achieves 69.83% global average accuracy, significantly outperforming competitors on social media and informal language contexts.

## Key Commands

### Core Pipeline
```bash
# Build the global dataset from raw sources (merges, deduplicates, splits)
python main.py build

# Preprocess/tokenize dataset for fast training (saves Arrow format)
python main.py preprocess

# Full training from base model (mDeBERTa-v3-base)
python main.py train [--epochs N] [--batch N] [--data PATH]

# Fine-tune existing model on specific dataset
python main.py finetune <csv> [--sample N] [--replay N] [--epochs N] [--batch N] [--lr N]

# Run benchmark against competitor models
python main.py benchmark

# Evaluate model on a benchmark CSV
python main.py evaluate [--data PATH]

# Interactive sentiment testing demo
python main.py demo
```

### Testing and Development
```bash
# Run a single test file
pytest tests/test_specific_module.py -v

# Run all tests
pytest tests/ -v
```

## Architecture

### Directory Structure
```
keloglan-sentiment/
├── main.py                      # CLI entry point - all commands flow through here
├── src/
│   ├── data/
│   │   ├── builder.py          # Merges raw datasets → global dataset
│   │   ├── preprocess.py       # Tokenizes and saves to Arrow format
│   │   ├── synthetic_factory.py  # Template-based synthetic data generation
│   │   ├── llm_augmentor.py    # LLM-powered data augmentation
│   │   └── data_manager.py     # Synthetic data management
│   ├── training/
│   │   └── trainer.py          # Unified KeloTrainer class (train + finetune)
│   ├── evaluation/
│   │   ├── benchmark.py        # BattleArena benchmark vs competitors
│   │   └── evaluator_3class.py # Detailed 3-class evaluation
│   └── utils/
│       ├── constants.py        # ALL configuration lives here
│       └── templates.py        # Template library for synthetic data
├── data/
│   ├── raw/                    # Original source datasets
│   ├── final/                  # Global train/val CSVs
│   ├── processed/              # Tokenized Arrow datasets
│   ├── benchmark/              # Benchmark datasets
│   └── synthetic/              # Generated synthetic data
└── models/                     # Trained model checkpoints
```

### Data Flow
1. **Raw Data Sources** (Winvoker, TRSAv1, WhiteAngelss, Product Reviews)
   → `DataBuilder.build()` → Merged & deduplicated CSV
2. **Global Dataset** → `preprocess_and_save()` → Tokenized Arrow (fast loading)
3. **Tokenized Data** → `KeloTrainer.train()` → Trained Model
4. **Trained Model** → `BattleArena.run()` / `Evaluator3Class` → Metrics

### Training Architecture

**KeloTrainer** (src/training/trainer.py) is a unified class supporting two modes:

1. **Full Training** (`train()`): Trains from base model on global dataset
   - Looks for pre-processed Arrow data first, falls back to CSV
   - Uses gradient accumulation for large effective batch size (64)
   - Supports early stopping and best model checkpointing

2. **Fine-tuning** (`finetune()`): Fine-tunes existing model on specific data
   - Includes replay samples from global dataset to prevent catastrophic forgetting
   - Lower learning rate (1e-5) and fewer epochs (1) by default

**Device Handling**: Automatically detects MPS (Apple Silicon) and falls back to CPU.

### Label System

Three-class classification: 0 (Negative), 1 (Neutral), 2 (Positive)

**Important**: Multiple label mappings exist in `constants.py`:
- `LABEL_MAP` / `REVERSE_LABEL_MAP`: Standard English labels
- `STRING_LABEL_MAP`: Handles mixed formats (Turkish "Notr", lowercase, numeric strings)
- `BENCHMARK_LABEL_MAP`: For Turkish benchmark labels ("Olumlu"/"Olumsuz")

Always use these mappings for consistency.

### Benchmark System

**BattleArena** (src/evaluation/benchmark.py) compares Keloğlan against:
- Savasy (BERT-base Turkish)
- Gorengoz (Winvoker-trained BERT)
- Incidelen (XLM-RoBERTa)
- And 5+ other Turkish sentiment models

The benchmark handles cross-compatibility between 2-class and 3-class models through label mapping.

## Configuration

**All configuration lives in `src/utils/constants.py`** - this is the single source of truth for:
- Model paths (BASE_MODEL, MODEL_DIR)
- Data paths (all directories)
- Training hyperparameters (BATCH_SIZE, LEARNING_RATE, etc.)
- Synthetic data generation (SYNTHETIC_COUNT, CATEGORY_WEIGHTS)
- Benchmark model list (BENCHMARK_MODELS)
- Hugging Face repos (HF_MODEL_REPO, HF_DATASET_REPO)

When adding new configuration, add it to `constants.py`, not scattered across files.

## Key Design Patterns

1. **Unified CLI**: All operations go through `main.py` subcommands - no direct script execution
2. **Centralized Config**: All constants in one file - no magic numbers
3. **Device Agnostic**: MPS detection with CPU fallback throughout
4. **Arrow Format**: Pre-tokenized datasets saved as Arrow for instant loading
5. **Replay Mechanism**: Fine-tuning includes global data samples to prevent forgetting
6. **Template-Based Generation**: Synthetic data uses rich template library with category weighting

## Turkish Language Nuances

The model specifically handles:
- **Irony/Sarcasm**: "Great (!) service indeed" → Negative
- **Cultural References**: "Silivri is cold right now" → Negative/Political
- **Gen-Z Slang**: "They ghosted me" → Negative
- **Mixed Labels**: Both Turkish ("Notr", "Olumlu") and English labels supported

Templates in `templates.py` cover: fashion, cosmetic, tech, student, art, 2ndhand, KS (Gen-Z slang), irony, cultural, gamer, relationships, food, and life contexts.
