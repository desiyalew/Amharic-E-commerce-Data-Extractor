class LendingScoreCard:
    @staticmethod
    def generate_score(avg_views, posting_freq, avg_price):
        # Custom scoring formula
        score = (avg_views * 0.5) + (posting_freq * 0.3) + (avg_price * 0.2)
        return round(score, 2)

    def create_vendor_summary(self, vendors):
        summary = []
        for name, data in vendors.items():
            score = self.generate_score(data["avg_views"], data["posting_freq"], data["avg_price"])
            summary.append({
                "Vendor": name,
                "Avg Views/Post": data["avg_views"],
                "Posts/Week": data["posting_freq"],
                "Avg Price (ETB)": data["avg_price"],
                "Lending Score": score
            })
        return summary