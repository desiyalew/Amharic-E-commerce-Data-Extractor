from transformers import AutoTokenizer

class TokenizerAligner:
    def __init__(self, model_name="xlm-roberta-base"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)

    def align_labels_with_tokens(self, examples):
        """
        Tokenizes input sentences and aligns NER labels with tokenized inputs.
        Handles subword tokenization and misalignment issues.
        """
        tokenized_inputs = self.tokenizer(
            examples["tokens"],
            truncation=True,
            padding="max_length",
            max_length=128,
            is_split_into_words=True,
        )

        aligned_labels = []
        for i, label in enumerate(examples["ner_tags"]):
            word_ids = tokenized_inputs.word_ids(batch_index=i)
            previous_word_idx = None
            label_ids = []

            for word_idx in word_ids:
                if word_idx is None:
                    label_ids.append(-100)
                elif word_idx >= len(label):  # Safety check
                    label_ids.append(-100)
                elif word_idx != previous_word_idx:
                    label_ids.append(label[word_idx])
                else:
                    label_ids.append(label[word_idx])
                previous_word_idx = word_idx
            aligned_labels.append(label_ids)

        tokenized_inputs["labels"] = aligned_labels
        return tokenized_inputs