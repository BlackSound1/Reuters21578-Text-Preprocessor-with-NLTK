from pathlib import Path
from typing import List, Optional

from typer import rich_utils
from typing_extensions import Annotated

import typer
from nltk import PorterStemmer

from file_writing import write_to_file

# Define certain colors and styles
rich_utils.OPTIONS_PANEL_TITLE = "[not dim]Options"
rich_utils.ARGUMENTS_PANEL_TITLE = "[not dim]Arguments"
rich_utils.STYLE_REQUIRED_LONG = 'not dim red'
rich_utils.STYLE_OPTION_DEFAULT = 'not dim white'

stemmer = typer.Typer(name="Stemmer", short_help="A Module for stemming all tokens in a given list.",
                      add_completion=False, rich_markup_mode='rich', no_args_is_help=True)


@stemmer.command(name='stem', short_help='Stems all tokens according to the Porter stemmer.',
                 rich_help_panel='COMMANDS', no_args_is_help=True, epilog="Thanks for using my stemmer! :boom:",
                 options_metavar='[--help]', help="""Stems all tokens according to the Porter stemmer.
                 
                 [not dim]
                 The arguments to this command are a list of tokens. These tokens are all stemmed using
                 NLTKs built-in Porter stemmer.
                 
                 It is possible to specify a custom file to save results to. Files should always look like: [bold yellow]<nested/directories/file.txt>[/].
                 Regardless of the nesting of directories and filename you specify, results will always be saved to the [bold yellow]output/[/] directory.
                   
                 For instance, running: 
                   
                 python stem.py interesting tokens are sometimes longer than others --file-path my_article/stem.txt
                   
                 will save to [bold yellow]output/my_article/stem.txt[/]
                 
                 [bold yellow]Example Usages[/]:
                 python stem.py interesting tokens are sometimes longer than others
                 python stem.py interesting tokens are sometimes longer than others --file-path my_article/stem.txt
                 """)
def stem(
        tokens: Annotated[List[str], typer.Argument(help="The tokens to use.", show_default=False)],
        article_num: Annotated[Optional[int], typer.Option(help="Declare which article number this should be.",
                                                           hidden=True)] = 0,
        file_path: Annotated[Path, typer.Option(help="Specify an optional file to save this result to.")] = Path(
            'custom_article/3. Stemmed-output.txt')

) -> List[str]:
    """
    Stem the given list of tokens for an article with the Porter stemmer

    :param tokens: The list of tokens to stem
    :param article_num: Which article this is
    :param file_path: A file path to save the file to. Must take form of directory/file.txt
    :return: The stemmed version of the list of tokens, stemmed using the Porter stemmer
    """

    # Create a default Porter stemmer
    STEMMER = PorterStemmer()

    # Stem each token in the given list of tokens with the Porter stemmer
    STEMMED: List[str] = [STEMMER.stem(token) for token in tokens]

    if not file_path:
        print(f"Article {article_num}: writing to file output/article{article_num}/4. Stemmed-output.txt")
        write_to_file(Path(f"article{article_num}/4. Stemmed-output.txt"), STEMMED)
    else:
        print(f"Custom article: writing to file output/{file_path}")
        write_to_file(file_path, STEMMED)

    return STEMMED


if __name__ == '__main__':
    stemmer()
