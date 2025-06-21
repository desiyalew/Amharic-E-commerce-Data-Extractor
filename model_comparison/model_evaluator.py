from sklearn.metrics import classification_report, f1_score

class ModelEvaluator:
    def evaluate_model(self, trainer, test_dataset):
        predictions = trainer.predict(test_dataset)
        preds = predictions.predictions.argmax(-1)
        true_labels = test_dataset["labels"]

        report = classification_report(true_labels.flatten(), preds.flatten())
        print(report)
        return {
            "f1_score": f1_score(true_labels.flatten(), preds.flatten(), average="weighted"),
            "classification_report": report
        }

    def compare_models(self, trained_models, test_dataset):
        results = {}
        for name, trainer in trained_models.items():
            print(f"Evaluating {name}...")
            result = self.evaluate_model(trainer, test_dataset)
            results[name] = result
        return results