from pathlib import Path
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
                   options_metavar='[--help]', no_args_is_help=True, epilog="Thanks for using my tokenizer! :boom:",
                   help="""Tokenizes the given text using the NLTK `word_tokenize()` method.
                   
                   [not dim]
                   Takes the given text as a string and tokenizes it according to the NLTK `word_tokenize()` method.
                   It is possible to specify a custom file to save results to. Files should always look like: [bold yellow]<nested/directories/file.txt>[/].
                   Regardless of the nesting of directories and filename you specify, results will always be saved to the [bold yellow]output/[/] directory.
                   
                   For instance, running: 
                   
                   python tokenization.py "This is some text" --file-path my_article/tokens.txt
                   
                   will save to [bold yellow]output/my_article/tokens.txt[/]
                   
                   [bold yellow]Example Usages[/]:
                   python tokenization.py "This is some text"
                   python tokenization.py "This is some text" --file-path my_article/tokens.txt
                   """)
def tokenize(
        text: Annotated[str, typer.Argument(help="The text to tokenize.", show_default=False)],
        article_num: Annotated[int, typer.Option(help="Which article in the corpus this is. Used in logging.",
                                                 hidden=True)] = 0,
        file_path: Annotated[Path, typer.Option(help="Specify an optional file to save this result to.")] = Path(
            'custom_article/1. Tokenizer-output')
) -> List[str]:
    """
    Tokenize the article text

    :param text: The article text to tokenize
    :param article_num: Which article this is
    :param file_path: A file path to save the file to. Must take form of directory/file.txt
    :return: A list of strings representing the tokens of the article
    """

    # Tokenize the given article text string
    TOKENIZED: List[str] = word_tokenize(text)

    if not file_path:
        print(f"Article {article_num}: writing to file output/article{article_num}/2. Tokenizer-output.txt")
        write_to_file(Path(f"article{article_num}/2. Tokenizer-output.txt"), TOKENIZED)
    else:
        print(f"Custom article: writing to file output/{file_path}")
        write_to_file(file_path, TOKENIZED)

    return TOKENIZED


if __name__ == '__main__':
    tokenizer()
