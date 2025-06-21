import re
import unicodedata

class AmharicTextProcessor:
    @staticmethod
    def normalize_text(text):
        # Normalize characters
        text = unicodedata.normalize("NFKC", text)
        return text

    @staticmethod
    def remove_non_amharic(text):
        # Keep only Amharic letters and common punctuation
        pattern = r'[^\u1200-\u137F\s.,?!፨፩፪]'
        return re.sub(pattern, '', text)

    @staticmethod
    def tokenize(text):
        # Basic space-based tokenization; replace with spacy if needed
        return text.split()

    def preprocess(self, text):
        text = self.normalize_text(text)
        text = self.remove_non_amharic(text)
        tokens = self.tokenize(text)
        return " ".join(tokens)