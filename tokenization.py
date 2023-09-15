from typing import List
from sys import argv

from nltk import word_tokenize

from file_writing import write_to_file


def tokenize(text: str, article_num: int, pipeline: bool = True) -> List[str]:
    """
    Tokenize the article text

    :param text: The article text to tokenize
    :param article_num: Which article this is
    :param pipeline: Whether this function is being run via the pipeline, or as a script
    :return: A list of strings representing the tokens of the article
    """

    # Tokenize the given article text string
    TOKENIZED: List[str] = word_tokenize(text)

    if pipeline:
        print(f"Article {article_num}: writing to file output/article{article_num}/Tokenizer-output.txt")
        write_to_file(article_num, "2. Tokenizer-output", TOKENIZED)
    else:
        print(f"Custom article: writing to file output/custom_article/Tokenizer-output.txt")
        write_to_file(article_num, "1. Tokenizer-output", TOKENIZED, custom=True)

    return TOKENIZED


if __name__ == '__main__':
    tokenize(text=argv[1], article_num=0, pipeline=False)
