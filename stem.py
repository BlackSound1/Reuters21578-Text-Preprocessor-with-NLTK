from typing import List

from nltk import PorterStemmer

from file_writing import write_to_file


def stem(text: List[str], article_num) -> List[str]:
    STEMMER = PorterStemmer()

    STEMMED: List[str] = [STEMMER.stem(token) for token in text]

    if article_num < 5:
        print(f"Article {article_num}: writing to file output/article{article_num}/Stemmed-output.txt")

        write_to_file(article_num, "Stemmed-output.txt", STEMMED)

    return STEMMED
