from typing import List
from pathlib import Path

from nltk import word_tokenize

from file_writing import write_to_file


def tokenize(text: str, article_num: int) -> List[str]:
    tokenized: List[str] = word_tokenize(text)

    if article_num < 5:
        print(f"Article {article_num}: writing to file Tokenizer-output")

        write_to_file(article_num, "Tokenizer-output", tokenized)

        # DIR_NAME = f"output/article{article_num}"
        #
        # FILENAME = f"{DIR_NAME}/Tokenizer-output.txt"
        #
        # Path(DIR_NAME).mkdir(parents=True, exist_ok=True)
        #
        # with open(FILENAME, "w+t", encoding="utf-8") as file:
        #     # Write each entry in the list line-by-line
        #     file.writelines([i + '\n' for i in tokenized])

    return tokenized
