from typing import List

from nltk import PorterStemmer


def stem(text: List[str], article_num) -> List[str]:
    STEMMER = PorterStemmer()

    STEMMED: List[str] = [STEMMER.stem(token) for token in text]

    if article_num < 5:
        print("Writing to file (STEM)")

    return STEMMED
