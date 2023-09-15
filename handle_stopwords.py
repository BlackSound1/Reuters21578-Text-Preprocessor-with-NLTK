from typing import List
from sys import argv

from file_writing import write_to_file


def remove_stopwords(tokens: List[str], article_num: int, stopwords_file: str, pipeline: bool = True):
    """
    As the final step, remove all words from the list of tokens that are stopwords

    :param tokens: The list of tokens to filter stopwords out of
    :param article_num: Which article this is
    :param pipeline: Whether this function is being run via the pipeline, or as a script
    :param stopwords_file: The file where stopwords are defined
    """

    # Read the given stopwords file and create a list of the stopwords within
    with open(stopwords_file, "r") as file:
        STOPWORDS: List[str] = [word.strip() for word in file.readlines()]

    # Filter out the stopwords
    FINAL: List[str] = [word for word in tokens if word not in STOPWORDS]

    if pipeline:
        print(f"Article {article_num}: writing to file output/article{article_num}/No-stopword-output.txt")
        write_to_file(article_num, "5. No-stopword-output", FINAL)
    else:
        print(f"Custom article: writing to file output/custom_article/No-stopword-output.txt")
        write_to_file(article_num, "4. No-stopword-output", FINAL, custom=True)


if __name__ == '__main__':
    remove_stopwords(tokens=argv[1:], article_num=0, stopwords_file="Stopwords-used-for-output.txt", pipeline=False)
