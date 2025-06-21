import shap

class SHAPInterpreter:
    def __init__(self, model, tokenizer):
        self.explainer = shap.Explainer(model, tokenizer)

    def explain_example(self, example):
        shap_values = self.explainer([example])
        shap.plots.waterfall(shap_values[0])