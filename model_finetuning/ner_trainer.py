from transformers import TrainingArguments, Trainer

class NERModelTrainer:
    def __init__(self, model_name="xlm-roberta-base", num_labels=7):
        from transformers import AutoModelForTokenClassification
        self.model = AutoModelForTokenClassification.from_pretrained(model_name, num_labels=num_labels)

    def train(self, tokenized_datasets, output_dir="./models"):
        training_args = TrainingArguments(
            output_dir=output_dir,
            learning_rate=2e-5,
            per_device_train_batch_size=16,
            num_train_epochs=3,
            weight_decay=0.01,
            evaluation_strategy="epoch",
            save_strategy="epoch"
        )

        trainer = Trainer(
            model=self.model,
            args=training_args,
            train_dataset=tokenized_datasets["train"],
            eval_dataset=tokenized_datasets["validation"]
        )
        trainer.train()
        return trainer