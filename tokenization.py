from typing import List
from typing_extensions import Annotated
from typer import rich_utils

from nltk import word_tokenize
import typer

from file_writing import write_to_file

# Define certain colors and styles
rich_utils.OPTIONS_PANEL_TITLE = "[not dim]Options"
rich_utils.ARGUMENTS_PANEL_TITLE = "[not dim]Arguments"
rich_utils.STYLE_REQUIRED_LONG = 'not dim red'
rich_utils.STYLE_OPTION_DEFAULT = 'not dim white'

tokenizer = typer.Typer(name="Tokenizer", short_help="A Module for tokenizing a given text.", add_completion=False,
                        rich_markup_mode="rich", no_args_is_help=True, options_metavar='[--help]')


@tokenizer.command(name="tokenize", short_help="Tokenize the given text.", rich_help_panel="COMMANDS",
                   options_metavar='[--pipeline | --help]', no_args_is_help=True, help="""
                   Tokenizes the given text using the NLTK `word_tokenize` method.
                   
                   [not dim]
                   Takes the given text as string and tokenizes it according to the NLTK `word_tokenize` method.
                   """)
def tokenize(
        text: Annotated[str, typer.Argument(help="The text to tokenize.", show_default=False)],
        article_num: Annotated[int, typer.Option(help="Which article in the corpus this is. Used in logging.",
                                                 hidden=True)] = 0,
        pipeline: Annotated[bool, typer.Option(help="Whether this function is being run in the normal pipeline,"
                                                    "or as a standalone CLI call.")] = True
) -> List[str]:
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
    tokenizer()
