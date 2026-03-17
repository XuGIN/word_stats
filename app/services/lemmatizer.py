import pymorphy3

_morph = None

def get_morph():
    global _morph
    if _morph is None:
        _morph = pymorphy3.MorphAnalyzer()
    return _morph

def lemmatize_word(word: str) -> str:
    morph = get_morph()

    return morph.parse(word)[0].normal_form