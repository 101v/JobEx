import jobex.strana.spacy_factory as spacy_factory

def tokenize(text: str):   
    tokens = []
    if text:
        text = text.lower()
        nlp = spacy_factory.get_spacy_nlp()
        doc = nlp(text)
        for token in doc:
            tokens.append(token.text)
    return tokens

# currently it is assumed that candidate can have at max 2 words.
# TODO: remove 2 words limitation
def find_matches(tokens, candidates):
    matched_candidates = []
    for candidate in candidates:
        candidate_parts = candidate.split()
        if len(candidate_parts) > 1:
            for i, x in enumerate(tokens):
                if candidate_parts[0] == tokens[i] and i < len(tokens)-1 and candidate_parts[1] == tokens[i + 1]:
                    matched_candidates.append(candidate)
        else:    
            if candidate in tokens:
                matched_candidates.append(candidate)
    
    return matched_candidates