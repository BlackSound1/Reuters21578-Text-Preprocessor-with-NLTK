from pathlib import Path
from typing import List, Optional
from typing_extensions import Annotated
from typer import rich_utils
import rich

from nltk import word_tokenize
import typer

from file_writing import write_to_file

# Define certain colors and styles
rich_utils.OPTIONS_PANEL_TITLE = "[not dim]Options"
rich_utils.ARGUMENTS_PANEL_TITLE = "[not dim]Arguments"
rich_utils.STYLE_REQUIRED_LONG = 'not dim red'
rich_utils.STYLE_OPTION_DEFAULT = 'not dim white'

# Define tokenizer app
tokenizer = typer.Typer(add_completion=False, rich_markup_mode="rich", no_args_is_help=True)

# Define certain app arguments and options. Makes later code cleaner
ARTICLE_NUM_OPTION = typer.Option(help="Which article in the corpus this is. Used in logging.", hidden=True)
FILE_OPTION = typer.Option("--file", "-f", help="Specify an optional file to save this result to.")


@tokenizer.command(short_help="Tokenize the given text.", rich_help_panel="COMMANDS", no_args_is_help=True,
                   options_metavar='[--help] [--file <dir/file.txt>]', epilog="Thanks for using my tokenizer! :boom:",
                   help="""Tokenizes the given text using the NLTK `word_tokenize()` method.
                   
                   [not dim]
                   Takes the given text as a string and tokenizes it according to the NLTK `word_tokenize()` method.
                   
                   It is possible to specify a custom file to save results to. Files should look like: [bold yellow]<nested/directories/file.txt>[/].
                   Regardless of the nesting of directories and filename you specify, results will always be saved to the [bold yellow]output/[/] directory.
                   
                   For instance, running: 
                   
                   python tokenization.py "This is some text" --file my_article/tokens.txt
                   
                   will save to [bold yellow]output/my_article/tokens.txt[/]. If no file is specified, it will save to
                   [bold yellow]output/custom_article/1. Tokenizer-output.txt[/]
                   
                   [bold yellow]Example Usages[/]:
                   python tokenization.py "This is some text"
                   python tokenization.py "This is some text" --file my_article/tokens.txt
                   """)
def tokenize(
        text: Annotated[str, typer.Argument(help="The text to tokenize, written in quotes.", show_default=False)],
        article_num: Annotated[int, ARTICLE_NUM_OPTION] = 0,
        file_path: Annotated[Optional[Path], FILE_OPTION] = None,
        pipeline: Annotated[bool, typer.Option(hidden=True)] = False
) -> List[str]:
    """
    Tokenize the article text

    :param text: The article text to tokenize
    :param article_num: Which article this is
    :param file_path: A file path to save the file to. Must take form of directory/file.txt
    :param pipeline: Whether this command is running as part of the pipeline. Changes file writing
    :return: A list of strings representing the tokens of the article
    """

    # Test to make sure the given token string isn't blank
    if not text:
        rich.print(f"\n[red bold]Blank text is not permitted.")
        raise typer.Exit(1)

    # Tokenize the given article text string
    TOKENIZED: List[str] = word_tokenize(text)

    # If this is running as the pipeline, this will be the 2nd file written
    if pipeline:
        file_print = Path(f'article{article_num}/2. Tokenizer-output.txt')
        rich.print(f"\twriting to file \"{'output' / file_print}\"")
        write_to_file(file_print, TOKENIZED)

    # If this is not running as the pipeline, this will be the 1st file written
    else:
        # If a file is specified, write to it
        if file_path:
            rich.print(f"\nCustom article: writing to file \"{'output' / file_path}\"")
            write_to_file(file_path, TOKENIZED)

        # If not, write to default location
        else:
            file_print = Path("custom_article/1. Tokenizer-output.txt")
            rich.print(f"\nCustom article: writing to file \"{'output' / file_print}\"")
            write_to_file(file_print, TOKENIZED)

        # When not in pipeline, print output to screen
        rich.print(f"\n[bold blue]Output:[/]\n{' '.join(t for t in TOKENIZED)}")

    return TOKENIZED


if __name__ == '__main__':
    tokenizer()
