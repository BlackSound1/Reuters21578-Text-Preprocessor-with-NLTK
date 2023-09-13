from typing import List

from nltk import PorterStemmer

from file_writing import write_to_file


def stem(tokens: List[str], article_num) -> List[str]:
    """
    Stem the given list of tokens for an article with the Porter stemmer

    :param tokens: The list of tokens to stem
    :param article_num: Which article this is
    :return: The stemmed version of the list of tokens, stemmed using the Porter stemmer
    """

    # Create a default Porter stemmer
    STEMMER = PorterStemmer()

    # Stem each token in the given list of tokens with the Porter stemmer
    STEMMED: List[str] = [STEMMER.stem(token) for token in tokens]

    print(f"Article {article_num}: writing to file output/article{article_num}/Stemmed-output.txt")

    write_to_file(article_num, "4. Stemmed-output.txt", STEMMED)

    return STEMMED
