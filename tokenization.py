from typing import List

from nltk import word_tokenize

from file_writing import write_to_file


def tokenize(text: str, article_num: int) -> List[str]:
    TOKENIZED: List[str] = word_tokenize(text)

    if article_num < 5:
        print(f"Article {article_num}: writing to file output/article{article_num}/Tokenizer-output.txt")

        write_to_file(article_num, "Tokenizer-output", TOKENIZED)

    return TOKENIZED
