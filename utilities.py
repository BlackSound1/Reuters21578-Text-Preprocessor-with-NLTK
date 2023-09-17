from glob import glob
from pathlib import Path
from re import sub
from typing import List

import rich
from rich.progress import Progress, SpinnerColumn
from bs4 import BeautifulSoup
from bs4.element import Tag

from file_writing import write_to_file


def get_all_texts(directory: str = "../reuters21578") -> List[Tag]:
    """
    Get all the articles in the corpus and return a list of them

    :param directory: Optionally specify where the reuters corpus is
    :return: A List of articles as `bs4.element.Tag` objects
    """

    # Create a list of file names in the required Reuters corpus
    CORPUS_FILES: List[Path] = [Path(p) for p in glob(f"{directory}/*.sgm")]

    rich.print("\nFound files:\n", [f"{f}" for f in CORPUS_FILES])

    # This will contain all the newspaper articles in the Reuters corpus
    all_articles: List[Tag] = []

    print()

    # Create a spinner to show that the app isn't frozen
    progress_bar = Progress(SpinnerColumn(), '[progress.description]{task.description}', SpinnerColumn(), transient=True)

    with progress_bar as progress:
        task = progress.add_task("Creating list of articles...")

        # Loop through each file
        for file in CORPUS_FILES:

            # Read the file contents
            with open(file, 'r') as f:
                contents = BeautifulSoup(f, features="html.parser")

            # Get all the articles for the file
            articles = contents('text')

            # Add each article to the list
            all_articles.extend(articles)

    # Verify number of articles
    rich.print(f"\nNumber of articles found: [bold green]{len(all_articles)}[/]\n")

    return all_articles


def textualize(article: Tag, article_num: int) -> str:
    """
    Take the given article (of type bs4.element.Tag) and turn it into normal text, as usable throughout the pipeline

    :param article: The article as a bs4.element.Tag
    :param article_num: Which article this is
    :return: The 'stringified' version of the article
    """

    # Bring all children together into 1 string
    text = '\n'.join(child.text for child in article.children)

    # Make sure all newline characters have a space after, to prevent future tokenization errors
    # as found in experiment
    text = text.replace('\n', '\n ')

    # Remove -- characters from one of the files
    text = sub(f'--', '', text)

    # Remove certain unicode control characters, as found in experiment
    text = sub(r'\x03|\x02', '', text)

    # Don't print or write to file for any articles beyond 5
    if article_num <= 5:
        # Write this semi-cleaned text to file
        file_print = Path(f'output/article{article_num}/1. Initial.txt')
        rich.print(f"\twriting to file \"{file_print}\"")
        write_to_file(Path(f"article{article_num}/1. Initial-text.txt"), text)

    return text
