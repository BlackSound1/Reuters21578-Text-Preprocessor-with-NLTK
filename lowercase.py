from typing import List, Optional

from typer import rich_utils
from typing_extensions import Annotated

import typer

from file_writing import write_to_file

# Define certain colors and styles
rich_utils.OPTIONS_PANEL_TITLE = "[not dim]Options"
rich_utils.ARGUMENTS_PANEL_TITLE = "[not dim]Arguments"
rich_utils.STYLE_REQUIRED_LONG = 'not dim red'
rich_utils.STYLE_OPTION_DEFAULT = 'not dim white'

lowercaser = typer.Typer(name='Lowercaser', short_help="A Module for making all tokens in a text lowercase.",
                         add_completion=False, rich_markup_mode='rich', no_args_is_help=True)


@lowercaser.command(name='lowercase', short_help="Makes all tokens lowercase.", rich_help_panel='COMMANDS',
                    options_metavar='[--help]', no_args_is_help=True,
                    epilog="Thanks for using my token lower-caser! :boom:", help="""
                    Makes all tokens lowercase.
                    
                    [not dim]
                    The arguments to this command are a list of tokens. These tokens are all made lowercase
                    
                    [bold yellow]Example Usage[/]:
                    python lowercase.py THESE ARE SOME TOKENS
                    """)
def lowercase(
        tokens: Annotated[List[str], typer.Argument(help="The tokens to use.", show_default=False)],
        article_num: Annotated[Optional[int], typer.Option(help="Declare which article number this should be.",
                                                           hidden=True)] = 0,
        pipeline: Annotated[bool, typer.Option(help='Whether this function is being run in the normal pipeline, '
                                                    'or as a standalone CLI call.', hidden=True)] = False
) -> List[str]:
    """
    Turn the tokens of the article all lowercase

    :param tokens: The list of tokens to make lowercase
    :param article_num: Which article this is
    :param pipeline: Whether this function is being run via the pipeline, or as a script
    :return: The list of tokens, all lowercase
    """

    # Create the lowercase version of the input tokens list
    LOWER_CASED: List[str] = [token.lower() for token in tokens]

    if pipeline:
        print(f"Article {article_num}: writing to file output/article{article_num}/Lowercased-output.txt")
        write_to_file(article_num, "3. Lowercased-output", LOWER_CASED)
    else:
        print(f"Custom article: writing to file output/custom_article/Lowercased-output.txt")
        write_to_file(article_num, "2. Lowercased-output", LOWER_CASED, custom=True)

    return LOWER_CASED


if __name__ == '__main__':
    lowercaser()
