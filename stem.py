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
                 options_metavar='[--help]', help="""
                 Stems all tokens according to the Porter stemmer.
                 
                 [not dim]
                 The arguments to this command are a list of tokens. These tokens are all stemmed using
                 NLTKs built-in Porter stemmer.
                 
                 [bold yellow]Example Usage[/]:
                 python stem.py interesting tokens are sometimes longer than others
                 """)
def stem(
        tokens: Annotated[List[str], typer.Argument(help="The tokens to use.", show_default=False)],
        article_num: Annotated[Optional[int], typer.Option(help="Declare which article number this should be.",
                                                           hidden=True)] = 0,
        pipeline: Annotated[bool, typer.Option(help='Whether this function is being run in the normal pipeline, '
                                                    'or as a standalone CLI call.', hidden=True)] = False
) -> List[str]:
    """
    Stem the given list of tokens for an article with the Porter stemmer

    :param tokens: The list of tokens to stem
    :param article_num: Which article this is
    :param pipeline: Whether this function is being run via the pipeline, or as a script
    :return: The stemmed version of the list of tokens, stemmed using the Porter stemmer
    """

    # Create a default Porter stemmer
    STEMMER = PorterStemmer()

    # Stem each token in the given list of tokens with the Porter stemmer
    STEMMED: List[str] = [STEMMER.stem(token) for token in tokens]

    if pipeline:
        print(f"Article {article_num}: writing to file output/article{article_num}/Stemmed-output.txt")
        write_to_file(article_num, "4. Stemmed-output", STEMMED)
    else:
        print(f"Custom article: writing to file output/custom_article/Stemmed-output.txt")
        write_to_file(article_num, "3. Stemmed-output", STEMMED, custom=True)

    return STEMMED


if __name__ == '__main__':
    stemmer()
