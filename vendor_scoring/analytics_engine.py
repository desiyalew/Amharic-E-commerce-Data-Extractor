from collections import defaultdict

class VendorAnalyticsEngine:
    def __init__(self, posts):
        self.posts = posts  # List of dicts with keys: text, views, date

    def calculate_posting_frequency(self):
        from datetime import datetime
        dates = [datetime.strptime(p['date'], "%Y-%m-%d %H:%M:%S") for p in self.posts]
        first_date = min(dates)
        last_date = max(dates)
        days_diff = (last_date - first_date).days
        return len(self.posts) / (days_diff or 1)

    def compute_avg_views(self):
        return sum(p['views'] for p in self.posts) / len(self.posts)

    def extract_prices(self, ner_model):
        prices = []
        for post in self.posts:
            tokens = post['text'].split()
            prediction = ner_model.predict(tokens)
            for token, tag in zip(tokens, prediction):
                if tag.startswith("B-PRICE"):
                    try:
                        prices.append(float(tag.split()[1]))
                    except:
                        pass
        return prices