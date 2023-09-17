from pathlib import Path
from typing import List, Optional
from typing_extensions import Annotated

import rich
import typer
from typer import rich_utils

from nltk import PorterStemmer

from file_writing import write_to_file

# Define certain colors and styles
rich_utils.OPTIONS_PANEL_TITLE = "[not dim]Options"
rich_utils.ARGUMENTS_PANEL_TITLE = "[not dim]Arguments"
rich_utils.STYLE_REQUIRED_LONG = 'not dim red'
rich_utils.STYLE_OPTION_DEFAULT = 'not dim white'

# Define stemmer app
stemmer = typer.Typer(add_completion=False, rich_markup_mode='rich', no_args_is_help=True)

# Define certain app arguments and options. Makes later code cleaner
ARTICLE_NUM_OPTION = typer.Option(help="Which article in the corpus this is. Used in logging.", hidden=True)
FILE_OPTION = typer.Option("--file", "-f", help="Specify an optional file to save this result to.")


@stemmer.command(short_help='Stems all tokens according to the Porter stemmer.', no_args_is_help=True,
                 epilog="Thanks for using my stemmer! :boom:", options_metavar='[--help] [--file <dir/file.txt>]',
                 help="""Stems all tokens according to the Porter stemmer.
                 
                 [not dim]
                 The arguments to this command are a list of tokens. These tokens are all stemmed using
                 NLTKs built-in Porter stemmer.
                 
                 It is possible to specify a custom file to save results to. Files should always look like: [bold yellow]<nested/directories/file.txt>[/].
                 Regardless of the nesting of directories and filename you specify, results will always be saved to the [bold yellow]output/[/] directory.
                   
                 For instance, running: 
                   
                 python stem.py interesting tokens are sometimes longer than others --file my_article/stem.txt
                   
                 will save to [bold yellow]output/my_article/stem.txt[/]. If no file is specified, it will save to
                 [bold yellow]output/custom_article/3. Stemmed-output.txt[/]
                 
                 [bold yellow]Example Usages[/]:
                 python stem.py interesting tokens are sometimes longer than others
                 python stem.py interesting tokens are sometimes longer than others --file my_article/stem.txt
                 """)
def stem(
        tokens: Annotated[List[str], typer.Argument(help="The tokens to use.", show_default=False)],
        article_num: Annotated[Optional[int], ARTICLE_NUM_OPTION] = 0,
        file_path: Annotated[Optional[Path], FILE_OPTION] = None,
        pipeline: Annotated[bool, typer.Option(hidden=True)] = False
) -> List[str]:
    """
    Stem the given list of tokens for an article with the Porter stemmer

    :param tokens: The list of tokens to stem
    :param article_num: Which article this is
    :param file_path: A file path to save the file to. Must take form of directory/file.txt
    :param pipeline: Whether this command is running as part of the pipeline. Changes file writing
    :return: The stemmed version of the list of tokens, stemmed using the Porter stemmer
    """

    # Ensure list of tokens is not blank
    if not all(token.strip() for token in tokens if token.strip() == ''):
        rich.print("\n[red bold]Empty list of tokens is not permitted.")
        raise typer.Exit(1)

    # Create a default Porter stemmer
    STEMMER = PorterStemmer()

    # Stem each token in the given list of tokens with the Porter stemmer
    STEMMED: List[str] = [STEMMER.stem(token) for token in tokens]

    # Don't print or write to file for any articles beyond 5
    if article_num <= 5:
        # If this is running as the pipeline, this will be the 4th file written
        if pipeline:
            file_print = Path(f"article{article_num}/4. Stemmed-output.txt")
            rich.print(f"\twriting to file \"{'output' / file_print}\"")
            write_to_file(file_print, STEMMED)

        # If this is not running as the pipeline, this will be the 3rd file written
        else:
            # If a file is specified, write to it
            if file_path:
                rich.print(f"\nCustom article: writing to file \"{'output' / file_path}\"")
                write_to_file(file_path, STEMMED)

            # If not, write to default location
            else:
                file_print = Path("custom_article/3. Stemmed-output.txt")
                rich.print(f"\nCustom article: writing to file \"{'output' / file_print}\"")
                write_to_file(file_print, STEMMED)

            # When not in pipeline, print output to screen
            rich.print(f"\n[bold blue]Output:[/]\n{' '.join(t for t in STEMMED)}")

    return STEMMED


if __name__ == '__main__':
    stemmer()
