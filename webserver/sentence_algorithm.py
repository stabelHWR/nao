from constants import POS_TOKENS, TAG_TOKENS
from word import Word

def sentence_detection(sentence):
    """
    Processes a sentence and extracts relevant words based on POS and TAG tokens.

    :param sentence: A list of tokenized words from the sentence.
    :return: A list of lemmas of the relevant words.
    """
    found_words = []
    for token in sentence:
        word = check_word(token)
        if word is not None:
            found_words.append(word)

    # Build list of lemmas which can be returned
    words = [word.get_lemma() for word in found_words]
    return words

def check_word(token):
    """
    Checks the POS of a token and decides whether to process it further.

    :param token: A token from the sentence.
    :return: A Word object if the token passes the POS check, else None.
    """
    if token.pos_ not in POS_TOKENS:
        return check_specific(token)
    else:
        return None

def check_specific(token):
    """
    Checks the TAG of a token and creates a Word object if it passes the check.

    :param token: A token from the sentence.
    :return: A Word object if the token passes the TAG check, else None.
    """
    if token.tag_ not in TAG_TOKENS:
        new_word = Word(token.pos_, token.tag_, token.lemma_, token.dep_)
        return new_word
    else:
        return None