from glob import glob
from pathlib import Path
from re import sub
from typing import List, Union

import rich
import typer
from rich.progress import Progress, SpinnerColumn
from bs4 import BeautifulSoup
from bs4.element import Tag

from file_writing import write_to_file


def get_texts(directory: str = "../reuters21578", article_count: Union[str, int] = 'all') -> List[Tag]:
    """
    Get any number of articles in the corpus and return a list of them

    :param directory: Optionally specify where the reuters corpus is
    :param article_count: How many articles to retrieve. "all" or a number >= 1
    :return: A List of articles as `bs4.element.Tag` objects
    """

    # Create a list of file names in the required Reuters corpus
    CORPUS_FILES: List[Path] = [Path(p) for p in glob(f"{directory}/*.sgm")]

    rich.print("\nFound files:\n", [f"{f}" for f in CORPUS_FILES])

    # This will contain all the newspaper articles in the Reuters corpus
    all_articles: List[Tag] = []

    print()

    # Create a spinner to show that the app isn't frozen
    spinner = Progress(SpinnerColumn(), '[progress.description]{task.description}', SpinnerColumn(), transient=True)

    with spinner:
        _ = spinner.add_task("Creating list of articles...")

        # Loop through each file
        for file in CORPUS_FILES:

            # Read the file contents
            with open(file, 'r') as f:
                contents = BeautifulSoup(f, features="html.parser")

            # Get all the articles for the file
            articles = contents('text')

            # Add each article to the list
            all_articles.extend(articles)

            # Stop adding to the list of articles once the desired number of articles is reached
            if article_count.isnumeric() and len(all_articles) >= int(article_count):
                break

    # If there is a definite article count provided, ensure article list only contains that many
    if article_count.isnumeric() and len(all_articles) > int(article_count):
        all_articles = all_articles[: int(article_count)]

    # Print a message if the user requested more articles than exist
    if article_count.isnumeric() and int(article_count) > len(all_articles):
        rich.print(f"You asked for [green bold]{article_count}[/] articles,"
                   f" but only [green bold]{len(all_articles)}[/] found\n")

    # In all other cases, just print the number of articles
    else:
        rich.print(f"Number of articles found: [bold green]{len(all_articles)}[/]\n")

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

    # Remove all instances of multiple - in a row
    text = sub(r'-{2,}', ' ', text)

    # Remove - characters without letters surrounding them. Keeps "once-in-a-lifetime", but not " - "
    text = sub(r'(?![A-Za-z])-(?![A-Za-z])', ' ', text)

    # Remove certain unicode control characters, as found in experiment
    text = sub(r'\x03|\x02', '', text)

    # Remove all punctuation except periods and commas. Handle those separately for money values
    text = sub(r"[()<>!:;?\"]+", ' ', text)

    # Remove all instances of multiple periods in a row
    text = sub(r"\.{2,}", ' ', text)

    # Simplify acronyms to their constituent letters. i.e. changes "U.S." to "US"
    text = sub(r"(?<!\w)([A-Za-z])\.", r'\1', text)

    # Remove all periods that aren't surrounded by a number. i.e. keeps "1.1" and "1."
    text = sub(r"(?!\d)\.(?!\d)", ' ', text)

    # Remove all commas that aren't surrounded by a number. i.e. keeps "1,000"
    text = sub(r"(?!\d),(?!\d)", ' ', text)

    # Remove all apostrophes surrounded by letters. In other words, replace all "it's" with "its", etc.
    text = sub(r"(?<=[A-Za-z])'(?=[A-Za-z])", '', text)

    # Remove all apostrophes remaining. (Needed to do this separately, because we needed to replace contraction
    # apostrophes with nothing. We will replace all other apostrophes with a space
    text = sub(r"'", ' ', text)

    # Remove all slashes, but not with numbers. For instance, removes / in "March/April", but not "1998/99".
    # I will treat numbers with slashes in them as 1 concept
    text = sub(r"(?!\d)/(?!\d)", ' ', text)

    file_print = Path(f'output/article{article_num}/1. Initial-text.txt')

    # Don't print for any articles beyond 5
    if article_num <= 5:
        rich.print(f"\twriting to file \"{file_print}\"")

    # Write this semi-cleaned text to file
    write_to_file(Path(f"article{article_num}/1. Initial-text.txt"), text)

    return text


def count_callback(count: str) -> str:
    """
    A callback function for the Pipeline Typer app, to validate user input.

    The value must either be "all" or a number >= 1.

    :param count: The value the user entered for the number of articles they want printed
    :return: The value, if it was valid
    """

    if not count.isnumeric() and count.lower() != 'all':
        rich.print("\n[red bold]Only \"all\" or a number are permitted[/]\n")
        raise typer.Exit(1)

    if count.isnumeric() and int(count) < 1:
        rich.print("\n[red bold]Only integers >= 1 are permitted[/]\n")
        raise typer.Exit(1)

    return count
