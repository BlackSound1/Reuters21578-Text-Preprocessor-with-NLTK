from pathlib import Path
from re import sub
from typing import List

from bs4 import BeautifulSoup
from bs4.element import Tag, NavigableString

from file_writing import write_to_file


def get_five_articles(input_file: str = "../reuters21578/reut2-000.sgm") -> List[str]:
    """
    Get the first five articles of the reuters 21578 corpus

    :param input_file: The file in the corpus containing the first 5 articles
    :return: A list of the first 5 articles
    """

    # Open the first sgm file
    with open(input_file, 'r') as file:
        soup = BeautifulSoup(file, 'html.parser')

    # Get only first 5 articles
    ARTICLES = soup('text')[:5]

    return ARTICLES


def textualize(article: Tag, article_num: int) -> str:
    """
    Take the given article (of type bs4.element.Tag) and turn it into normal text, as usable throughout the pipeline

    :param article: The article as a bs4.element.Tag
    :param article_num: Which article this is
    :return: The 'stringified' version of the article
    """

    # Create a list of child elements for this article,
    # making sure that they're all Tag elements. Important for later
    CHILDREN = [child for child in article.children if type(child) is not NavigableString]

    # Bring all children together into 1 string
    text = '\n'.join(child.text for child in CHILDREN)

    # Make sure all newline characters have a space after, to prevent future tokenization errors
    # as found in experiment
    text = text.replace('\n', '\n ')

    # Remove -- characters from one of the files
    text = sub(f'--', '', text)

    # Remove certain unicode control characters, as found in experiment
    text = sub(r'\x03|\x02', '', text)

    # Write this semi-cleaned text to file
    write_to_file(Path(f"article{article_num}/1. Initial-text"), text)

    return text
