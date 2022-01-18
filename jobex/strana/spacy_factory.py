import spacy

nlp = spacy.load('en_core_web_sm')

def get_spacy_nlp():
    return nlp