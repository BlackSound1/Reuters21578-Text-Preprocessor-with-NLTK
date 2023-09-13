from typing import List

from file_writing import write_to_file


def remove_stopwords(tokens: List[str], article_num: int, stopwords_file: str):
    """
    As the final step, remove all words from the list of tokens that are stopwords

    :param tokens: The list of tokens to filter stopwords out of
    :param article_num: Which article this is
    :param stopwords_file: The file where stopwords are defined
    """

    # Read the given stopwords file and create a list of the stopwords within
    with open(stopwords_file, "r") as file:
        STOPWORDS: List[str] = [word.strip() for word in file.readlines()]

    # Filter out the stopwords
    FINAL: List[str] = [word for word in tokens if word not in STOPWORDS]

    print(f"Article {article_num}: writing to file output/article{article_num}/No-stopword-output.txt")

    # Write the final file
    write_to_file(article_num, "5. No-stopword-output.txt", FINAL)
