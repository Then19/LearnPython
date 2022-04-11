import re


def validate_fname_lname(text):
    pattern = r'[а-яё]+\s+[а-яё]+'
    check_text = re.fullmatch(pattern, text, re.IGNORECASE)
    return False if check_text is None else True

