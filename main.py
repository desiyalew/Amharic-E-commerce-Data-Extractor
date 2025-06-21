import asyncio
import platform

from data_ingestion.telegram_scraper import TelegramScraper
from data_ingestion.amharic_preprocessor import AmharicTextProcessor
from dataset_labeling.conll_formatter import CoNLLLabeler
from model_finetuning.hf_dataset_utils import load_conll_to_hf_dataset
from model_finetuning.tokenizer_aligner import TokenizerAligner
from model_finetuning.ner_trainer import NERModelTrainer
from model_comparison.model_evaluator import ModelEvaluator
from vendor_scoring.analytics_engine import VendorAnalyticsEngine
from vendor_scoring.lending_scorecard import LendingScoreCard
from utils.config_loader import load_config
from utils.file_handler import write_json


def main():
    try:
        config = load_config()
    except Exception as e:
        print(f"[ERROR] Failed to load config: {e}")
        return

    # Step 1: Telegram Scraping
    try:
        print("[INFO] Setting up Telegram client...")
        
        # Manually create and set event loop
        if platform.system() == 'Windows':
            loop = asyncio.SelectorEventLoop()
            asyncio.set_event_loop(loop)
        else:
            loop = asyncio.get_event_loop()

        scraper = TelegramScraper(**config["telegram"])

        print("[INFO] Logging into Telegram...")
        loop.run_until_complete(scraper.login())

        print(f"[INFO] Fetching messages from channels: {config['channels']}")
        raw_messages = loop.run_until_complete(
            scraper.fetch_messages_from_channels(config["channels"])
        )

        scraper.save_messages_to_file(raw_messages, config["paths"]["raw_data"] + "raw_messages.json")
        print(f"[INFO] Raw messages saved to {config['paths']['raw_data']}")
    except Exception as e:
        print(f"[ERROR] Telegram scraping failed: {e}")
        return

    # Step 2: Preprocessing
    try:
        processor = AmharicTextProcessor()
        cleaned_messages = [
            {"text": processor.preprocess(msg["text"]), **msg} for msg in raw_messages
        ]
        write_json(cleaned_messages, config["paths"]["processed_data"] + "cleaned_messages.json")
        print(f"[INFO] Cleaned messages saved to {config['paths']['processed_data']}")
    except Exception as e:
        print(f"[ERROR] Text preprocessing failed: {e}")
        return

    # Step 3: Labeling (manual step skipped here; assumed done separately)
    # labeler = CoNLLLabeler()
    # labeler.export_to_conll(labeled_sentences, config["paths"]["labeled_data"] + "labeled_data.conll")

    # Step 4: Load Dataset
    try:
        print(f"[INFO] Loading labeled dataset from {config['paths']['labeled_data']}labeled_data.conll")
        label_list = ["O", "B-PRODUCT", "I-PRODUCT", "B-PRICE", "I-PRICE", "B-LOC", "I-LOC"]
        label_to_id = {label: i for i, label in enumerate(label_list)}
        dataset = load_conll_to_hf_dataset(config["paths"]["labeled_data"] + "labeled_data.conll", label_to_id)
        aligner = TokenizerAligner()
        tokenized_dataset = dataset.map(aligner.align_labels_with_tokens, batched=True)
    except Exception as e:
        print(f"[ERROR] Failed to load or tokenize dataset: {e}")
        return

    # Step 5: Train Models
    try:
        print("[INFO] Training XLM-Roberta model...")
        trainer_xlmr = NERModelTrainer(model_name="xlm-roberta-base", num_labels=len(label_list)).train(tokenized_dataset)

        print("[INFO] Training BERT-Amharic model...")
        trainer_bert = NERModelTrainer(model_name="bert-tiny-amharic", num_labels=len(label_list)).train(tokenized_dataset)
    except Exception as e:
        print(f"[ERROR] Model training failed: {e}")
        return

    # Step 6: Evaluate Models
    try:
        evaluator = ModelEvaluator()
        results = evaluator.compare_models({
            "XLM-Roberta": trainer_xlmr,
            "BERT-Amharic": trainer_bert
        })
        print("[INFO] Model Comparison Results:")
        for name, metric in results.items():
            print(f"{name}: F1 Score = {metric['f1_score']:.4f}")
    except Exception as e:
        print(f"[ERROR] Model evaluation failed: {e}")

    # Step 7: Vendor Analytics
    try:
        sample_posts = [p for p in cleaned_messages if p["channel"] == "@shageronlinestore"]
        analytics = VendorAnalyticsEngine(sample_posts)

        avg_views = analytics.compute_avg_views()
        posting_freq = analytics.calculate_posting_frequency()
        prices = analytics.extract_prices(trainer_xlmr)

        if len(prices) > 0:
            avg_price = sum(prices) / len(prices)
        else:
            avg_price = 0
    except Exception as e:
        print(f"[ERROR] Vendor analytics failed: {e}")
        return

    # Step 8: Generate Lending Score
    try:
        scorecard = LendingScoreCard()
        summary = scorecard.create_vendor_summary({
            "ShagerOnlineStore": {
                "avg_views": avg_views,
                "posting_freq": posting_freq,
                "avg_price": avg_price
            }
        })

        print("\n[INFO] Vendor Lending Score Summary:")
        for entry in summary:
            print(entry)
    except Exception as e:
        print(f"[ERROR] Failed to generate lending score: {e}")


if __name__ == "__main__":
    main()