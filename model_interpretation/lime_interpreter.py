from lime.lime_text import LimeTextExplainer

class LIMEInterpreter:
    def __init__(self, model, tokenizer, class_names):
        self.explainer = LimeTextExplainer(class_names=class_names)

    def explain_prediction(self, text, predict_fn):
        exp = self.explainer.explain_instance(text, predict_fn, num_features=6)
        exp.show_in_notebook()