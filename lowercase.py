from typing import List
from sys import argv

from file_writing import write_to_file


def lowercase(tokens: List[str], article_num: int, pipeline: bool = True) -> List[str]:
    """
    Turn the tokens of the article all lowercase

    :param tokens: The list of tokens to make lowercase
    :param article_num: Which article this is
    :param pipeline: Whether this function is being run via the pipeline, or as a script
    :return: The list of tokens, all lowercase
    """

    # Create the lowercase version of the input tokens list
    LOWER_CASED: List[str] = [token.lower() for token in tokens]

    if pipeline:
        print(f"Article {article_num}: writing to file output/article{article_num}/Lowercased-output.txt")
        write_to_file(article_num, "3. Lowercased-output", LOWER_CASED)
    else:
        print(f"Custom article: writing to file output/custom_article/Lowercased-output.txt")
        write_to_file(article_num, "2. Lowercased-output", LOWER_CASED, custom=True)

    return LOWER_CASED


if __name__ == '__main__':
    lowercase(tokens=argv[1:], article_num=0, pipeline=False)
