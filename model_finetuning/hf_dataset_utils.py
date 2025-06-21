from datasets import Dataset

def load_conll_to_hf_dataset(conll_path, label_to_id):
    """
    Load CoNLL file and convert string labels to integer IDs.
    """
    sentences = []
    labels = []
    
    with open(conll_path, 'r', encoding='utf-8') as f:
        tokens = []
        tags = []
        for line in f:
            line = line.strip()
            if not line:
                if tokens:
                    sentences.append(tokens)
                    labels.append([label_to_id[tag] for tag in tags])
                    tokens = []
                    tags = []
            elif len(line.split()) == 2:
                token, tag = line.split()
                tokens.append(token)
                tags.append(tag)
        # Handle last sentence if exists
        if tokens:
            sentences.append(tokens)
            labels.append([label_to_id[tag] for tag in tags])

    return Dataset.from_dict({"tokens": sentences, "ner_tags": labels})