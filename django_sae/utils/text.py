# coding=utf-8


def any_in(words, text):
    """ Check list of words in another string
    """
    for word in words:
        if word in text:
            return True
    return False