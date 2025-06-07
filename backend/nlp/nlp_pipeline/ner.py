from transformers import pipeline

# Load NER model
ner_pipeline = pipeline(
    "ner",
    model="dbmdz/bert-large-cased-finetuned-conll03-english",
    aggregation_strategy="simple",
)

def extract_entities(text, entity_labels=None):
    try:
        raw = ner_pipeline(text)
        entities = []
        for ent in raw:
            if "word" in ent and (not entity_labels or ent["entity_group"] in entity_labels):
                entities.append(ent["word"].replace(" ##", "").strip())
        return list(set(entities))
    except Exception as e:
        print(f"[NER] Error: {e}")
        return []
