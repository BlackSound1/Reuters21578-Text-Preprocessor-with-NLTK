from glob import glob
from bs4 import BeautifulSoup

from typing import List
import unicodedata


def fix_encoding_mistakes(text: str) -> str:
    """
    Fix certain mistakes that occur when reading .sgm files.

    When reading the .sgm files, due to encoding, there are some objective mistakes.
    For instance, < and > are replaced to lt; and gt;. Replace these to their correct values.

    :param text: The text to fix encoding mistakes for
    :return: The fixed string
    """

    # Removes control characters. Taken from https://stackoverflow.com/a/19016117
    text = "".join(ch for ch in text if unicodedata.category(ch)[0] != "C")

    if "&lt;" in text:
        text = text.replace("&lt;", "<")

    if "&gt;" in text:
        text = text.replace("&gt;", ">")

    return text


def get_all_texts(directory: str = "../reuters21578") -> List[str]:
    # Create a list of file names in the required Reuters corpus
    CORPUS_FILES: List[str] = glob(f"{directory}/*.sgm")

    print("\nFound files:\n", CORPUS_FILES)

    # This will contain all the newspaper articles in the Reuters corpus
    all_articles = []

    # Loop through each file
    for file in CORPUS_FILES:
        with open(file, 'r') as f:
            # Read the file contents
            contents = BeautifulSoup(f, features="html.parser")

            # Get all the articles for the file
            articles = contents('text')

            # Add each article to the list
            all_articles.extend(articles)

    # Verify number of articles
    print(f"Number of articles found: {len(all_articles)}")

    # print(all_articles)

    return all_articles
