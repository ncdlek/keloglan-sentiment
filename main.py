"""
🧙‍♂️ Keloğlan Sentiment Analysis CLI

Usage:
    python main.py build              Build the global dataset
    python main.py preprocess         Tokenize dataset for fast loading
    python main.py train              Full training from base model
    python main.py finetune <csv>     Fine-tune on a specific dataset
    python main.py hardmine           Hard Example Mining with LLM
    python main.py llmverify          LLM verification (FINAL AUTHORITY on labels!)
    python main.py benchmark          Run benchmark against competitors
    python main.py evaluate [csv]     Evaluate model on a benchmark
    python main.py demo               Interactive sentiment testing
"""

import argparse
import sys
import os
import pandas as pd

# Ensure src is importable
sys.path.insert(0, os.path.dirname(__file__))


def main():
    parser = argparse.ArgumentParser(
        description="🧙‍♂️ Keloğlan Sentiment CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # ── build ──────────────────────────────────────────────────────────────
    subparsers.add_parser("build", help="Build the global dataset from raw sources")

    # ── preprocess ─────────────────────────────────────────────────────────
    subparsers.add_parser("preprocess", help="Tokenize dataset for fast training")

    # ── train ──────────────────────────────────────────────────────────────
    p_train = subparsers.add_parser("train", help="Train model from scratch")
    p_train.add_argument("--epochs", type=int, default=None, help="Number of epochs")
    p_train.add_argument("--batch", type=int, default=None, help="Batch size")
    p_train.add_argument("--data", type=str, default=None, help="Optional custom dataset path")

    # ── finetune ───────────────────────────────────────────────────────────
    p_ft = subparsers.add_parser("finetune", help="Fine-tune on a specific CSV dataset")
    p_ft.add_argument("data", type=str, help="Path to fine-tuning CSV")
    p_ft.add_argument("--sample", type=int, default=None, help="Number of samples to use")
    p_ft.add_argument("--replay", type=int, default=10000, help="Replay samples to prevent forgetting")
    p_ft.add_argument("--epochs", type=int, default=None, help="Number of epochs")
    p_ft.add_argument("--batch", type=int, default=16, help="Batch size")
    p_ft.add_argument("--lr", type=float, default=None, help="Learning rate")

    # ── benchmark ──────────────────────────────────────────────────────────
    subparsers.add_parser("benchmark", help="Run benchmark against competitors")

    # ── evaluate ───────────────────────────────────────────────────────────
    p_eval = subparsers.add_parser("evaluate", help="Evaluate model on a benchmark CSV")
    p_eval.add_argument("--data", type=str, default=None, help="Path to benchmark CSV")

    # ── demo ───────────────────────────────────────────────────────────────
    subparsers.add_parser("demo", help="Interactive sentiment testing")

    # ── hardmine (Hard Example Mining) ─────────────────────────────────────
    p_mine = subparsers.add_parser("hardmine", help="Hard Example Mining with LLM")
    p_mine.add_argument("--model", type=str, default="models/keloglan-sentiment",
                       help="Path to trained model")
    p_mine.add_argument("--data", type=str,
                       default="data/final/keloglan_global_sentiment_val.csv",
                       help="Path to validation data for analysis")
    p_mine.add_argument("--mode", type=str, choices=["analyze", "generate", "curriculum"],
                       default="curriculum", help="Pipeline mode")
    p_mine.add_argument("--sample", type=int, default=1000,
                       help="Number of samples to analyze")
    p_mine.add_argument("--num-synthetic", type=int, default=50,
                       help="Number of synthetic examples per pattern")
    p_mine.add_argument("--output", type=str,
                       default="data/synthetic/hard_examples_v1.csv",
                       help="Output path for synthetic examples")

    # ── cleannoise (Label Noise Detection) ────────────────────────────────
    p_clean = subparsers.add_parser("cleannoise",
                                    help="Detect and clean label noise from dataset")
    p_clean.add_argument("--data", type=str, required=True,
                        help="Path to dataset CSV to clean")
    p_clean.add_argument("--mode", type=str, choices=["detect", "clean", "review"],
                       default="detect", help="Mode: detect=analyze, clean=remove/correct, review=interactive")
    p_clean.add_argument("--threshold", type=float, default=0.7,
                       help="Noise probability threshold (0-1)")
    p_clean.add_argument("--auto-correct", action="store_true",
                       help="Auto-correct labels using ensemble prediction")
    p_clean.add_argument("--output", type=str,
                       default="data/final/keloglan_cleaned_dataset.csv",
                       help="Output path for cleaned dataset")

    # ── llmverify (LLM Label Verification - FINAL AUTHORITY) ─────────────
    p_verify = subparsers.add_parser("llmverify",
                                     help="LLM verification - Final authority on label correctness (handles irony/slang!)")
    p_verify.add_argument("--data", type=str, required=True,
                         help="Path to dataset CSV")
    p_verify.add_argument("--mode", type=str, choices=["verify", "smart-clean", "hard-examples", "teaching"],
                         default="smart-clean", help="Verification mode")
    p_verify.add_argument("--sample", type=int, default=500,
                         help="Max examples to verify with LLM")
    p_verify.add_argument("--threshold", type=float, default=0.6,
                         help="Noise probability threshold for LLM verification")
    p_verify.add_argument("--llm-confidence", type=float, default=0.7,
                         help="LLM confidence threshold for auto-correction")
    p_verify.add_argument("--parallel", action="store_true",
                         help="Use parallel processing (faster, more CPU)")
    p_verify.add_argument("--workers", type=int, default=3,
                         help="Number of parallel workers for LLM calls")
    p_verify.add_argument("--output", type=str,
                         default="data/final/keloglan_llm_verified.csv",
                         help="Output path")

    args = parser.parse_args()

    # ── Dispatch ───────────────────────────────────────────────────────────
    if args.command == "build":
        from src.data.builder import DataBuilder
        DataBuilder().build()

    elif args.command == "preprocess":
        from src.data.preprocess import preprocess_and_save
        preprocess_and_save()

    elif args.command == "train":
        from src.training.trainer import KeloTrainer
        KeloTrainer().train(
            epochs=args.epochs,
            batch_size=args.batch,
            custom_data_path=args.data
        )

    elif args.command == "finetune":
        from src.training.trainer import KeloTrainer
        KeloTrainer().finetune(
            data_path=args.data,
            sample_n=args.sample,
            replay_n=args.replay,
            epochs=args.epochs,
            batch_size=args.batch,
            learning_rate=args.lr
        )

    elif args.command == "benchmark":
        from src.evaluation.benchmark import BattleArena
        BattleArena().run()

    elif args.command == "evaluate":
        from src.evaluation.evaluator_3class import Evaluator3Class
        Evaluator3Class().evaluate(csv_path=args.data)

    elif args.command == "demo":
        _run_demo()

    elif args.command == "hardmine":
        from src.data.hard_example_miner import HardExampleMiner
        miner = HardExampleMiner(args.model)

        df = pd.read_csv(args.data)
        if args.sample and len(df) > args.sample:
            df = df.sample(args.sample, random_state=42)

        if args.mode == "analyze":
            misclassified = miner.find_misclassified(df, sample_size=None)
            miner.analyze_error_patterns(misclassified)
            misclassified.to_csv(args.output.replace(".csv", "_misclassified.csv"), index=False)
            print(f"📄 Saved to {args.output.replace('.csv', '_misclassified.csv')}")

        elif args.mode == "generate":
            misclassified = miner.find_misclassified(df, sample_size=200)
            miner.generate_hard_examples_with_llm(
                misclassified,
                num_per_pattern=args.num_synthetic,
                output_path=args.output
            )

        elif args.mode == "curriculum":
            misclassified = miner.find_misclassified(df, sample_size=200)
            synthetic = miner.generate_hard_examples_with_llm(
                misclassified,
                num_per_pattern=args.num_synthetic,
                output_path=args.output
            )
            if not synthetic.empty:
                miner.create_curriculum_dataset(
                    df,
                    synthetic,
                    output_path="data/final/keloglan_curriculum_dataset.csv"
                )

    elif args.command == "cleannoise":
        from src.data.label_noise_detector import LabelNoiseDetector, InteractiveLabelReviewer
        import json

        detector = LabelNoiseDetector()

        if args.mode == "detect":
            report = detector.generate_correction_report(
                pd.read_csv(args.data),
                output_path=args.output.replace('.csv', '_report.json')
            )

            print(f"\n📊 NOISE SUMMARY:")
            print(f"   Total examples: {report['summary']['total_examples']}")
            print(f"   Potential noise: {report['summary']['potential_noise_count']}")
            print(f"   Noise rate: {report['summary']['noise_rate']*100:.1f}%")

        elif args.mode == "clean":
            cleaned_df, noise_df = detector.create_cleaned_dataset(
                pd.read_csv(args.data),
                output_path=args.output,
                noise_threshold=args.threshold,
                auto_correct=args.auto_correct
            )

        elif args.mode == "review":
            report_path = args.output.replace('.csv', '_report.json')
            if os.path.exists(report_path):
                with open(report_path, 'r', encoding='utf-8') as f:
                    report = json.load(f)
            else:
                report = detector.generate_correction_report(
                    pd.read_csv(args.data),
                    output_path=report_path
                )

            df = pd.read_csv(args.data)
            reviewer = InteractiveLabelReviewer(df, report)
            corrections = reviewer.review_interactive(max_reviews=50)

            if corrections:
                reviewer.apply_corrections(args.output)

    elif args.command == "llmverify":
        from src.data.llm_verifier import LLMLabelVerifier, SmartLabelCleaner

        df = pd.read_csv(args.data)
        print(f"✅ Loaded {len(df)} examples")

        if args.mode == "smart-clean":
            cleaner = SmartLabelCleaner()
            cleaned_df, report = cleaner.clean_dataset_smart(
                df,
                ensemble_threshold=args.threshold,
                llm_confidence_threshold=args.llm_confidence,
                verify_sample_size=args.sample,
                parallel=args.parallel,
                max_workers=args.workers,
                output_path=args.output
            )

        elif args.mode == "verify":
            verifier = LLMLabelVerifier()
            cleaned_df, verification_df = verifier.verify_and_clean_dataset(
                df,
                sample_size=args.sample,
                confidence_threshold=args.llm_confidence,
                parallel=args.parallel,
                max_workers=args.workers,
                output_path=args.output
            )

        elif args.mode == "teaching":
            from src.data.label_noise_detector import LabelNoiseDetector

            detector = LabelNoiseDetector()
            verifier = LLMLabelVerifier()

            result_df = detector.detect_ensemble_disagreement(df, sample_size=200)
            hard_examples = result_df[result_df['noise_probability'] > 0.6]

            verification_df = verifier.verify_batch(
                hard_examples.head(args.sample).to_dict('records')
            )

            teaching_df = verifier.generate_teaching_examples(
                verification_df,
                output_path=args.output.replace('.csv', '_teaching.csv')
            )

    else:
        parser.print_help()


def _run_demo():
    """Interactive demo — test sentiment on any Turkish text."""
    from transformers import pipeline
    from src.utils import constants

    model_path = constants.MODEL_DIR
    if not os.path.exists(model_path):
        print(f"❌ Model not found: {model_path}")
        print("   Run 'python main.py train' first.")
        return

    print("🧙‍♂️ Keloğlan Interactive Demo")
    print("─" * 40)
    print("Loading model...")

    try:
        analyzer = pipeline("sentiment-analysis", model=model_path)
    except Exception as e:
        print(f"❌ Error: {e}")
        return

    print("✅ Ready! Type 'exit' to quit.\n")

    while True:
        text = input("📝 Cümle: ")
        if text.lower() == 'exit':
            break
        if not text.strip():
            continue

        result = analyzer(text)[0]
        label = result['label']
        score = result['score']
        emoji = {"Positive": "😊", "Negative": "😡", "Neutral": "😐"}.get(label, "🤔")
        print(f"🤖 {label} {emoji} (confidence: {score * 100:.1f}%)\n")


if __name__ == "__main__":
    main()