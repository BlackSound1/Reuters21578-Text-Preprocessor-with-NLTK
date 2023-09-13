from typing import List

from file_writing import write_to_file


def remove_stopwords(text: List[str], article_num: int, stopwords_file: str) -> List[str]:
    # Read the given stopwords file
    with open(stopwords_file, "r") as file:
        STOPWORDS: List[str] = [word.strip() for word in file.readlines()]

    FINAL: List[str] = [word for word in text if word not in STOPWORDS]

    if article_num < 5:
        print(f"Article {article_num}: writing to file output/article{article_num}/No-stopword-output.txt")

        write_to_file(article_num, "No-stopword-output.txt", FINAL)

    return FINAL
