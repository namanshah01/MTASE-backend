from transformers import PegasusForConditionalGeneration, PegasusTokenizer

tokenizer_model = PegasusTokenizer.from_pretrained("google/pegasus-xsum")
loaded_model = PegasusForConditionalGeneration.from_pretrained("google/pegasus-xsum")

def abstractive_summariser(DOCUMENT):
    text = DOCUMENT

    # Create tokens - number representation of our text
    tokens = tokenizer_model(text, truncation=True, padding="longest", return_tensors="pt")

    summary = loaded_model.generate(**tokens)
    abstractive_summary = tokenizer_model.decode(summary[0])
    
    return (abstractive_summary)