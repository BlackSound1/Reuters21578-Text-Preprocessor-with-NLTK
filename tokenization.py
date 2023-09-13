from typing import List

from nltk import word_tokenize

from file_writing import write_to_file


def tokenize(text: str, article_num: int) -> List[str]:
    """
    Tokenize the article text

    :param text: The article text to tokenize
    :param article_num: Which article this is
    :return: A list of strings representing the tokens of the article
    """

    # Tokenize the given article text string
    TOKENIZED: List[str] = word_tokenize(text)

    print(f"Article {article_num}: writing to file output/article{article_num}/Tokenizer-output.txt")

    write_to_file(article_num, "2. Tokenizer-output", TOKENIZED)

    return TOKENIZED
