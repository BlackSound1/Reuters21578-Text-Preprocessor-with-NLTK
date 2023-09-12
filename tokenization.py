from typing import List

from nltk import word_tokenize

from file_writing import write_to_file


def tokenize(text: str, article_num: int) -> List[str]:
    tokenized: List[str] = word_tokenize(text)

    if article_num < 5:
        print(f"Article {article_num}: writing to file Tokenizer-output")

        write_to_file(article_num, "Tokenizer-output", tokenized)

    return tokenized
