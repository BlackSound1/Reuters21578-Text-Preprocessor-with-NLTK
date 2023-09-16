from pathlib import Path
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
                    epilog="Thanks for using my token lower-caser! :boom:", help="""Makes all tokens lowercase.
                    
                    [not dim]
                    The arguments to this command are a list of tokens. These tokens are all made lowercase
                    
                    It is possible to specify a custom file to save results to. Files should always look like: [bold yellow]<nested/directories/file.txt>[/].
                    Regardless of the nesting of directories and filename you specify, results will always be saved to the [bold yellow]output/[/] directory.
                   
                    For instance, running: 
                   
                    python lowercase.py THESE ARE SOME TOKENS --file-path my_article/lowercase.txt
                   
                    will save to [bold yellow]output/my_article/lowercase.txt[/]
                   
                    [bold yellow]Example Usages[/]:
                    python lowercase.py THESE ARE SOME TOKENS
                    python lowercase.py THESE ARE SOME TOKENS --file-path my_article/lowercase.txt
                    """)
def lowercase(
        tokens: Annotated[List[str], typer.Argument(help="The tokens to use.", show_default=False)],
        article_num: Annotated[Optional[int], typer.Option(help="Declare which article number this should be.",
                                                           hidden=True)] = 0,
        file_path: Annotated[Path, typer.Option(help="Specify an optional file to save this result to.")] = Path(
            'custom_article/2. Lowercased-output.txt')
) -> List[str]:
    """
    Turn the tokens of the article all lowercase

    :param tokens: The list of tokens to make lowercase
    :param article_num: Which article this is
    :param file_path: A file path to save the file to. Must take form of directory/file.txt
    :return: The list of tokens, all lowercase
    """

    # Create the lowercase version of the input tokens list
    LOWER_CASED: List[str] = [token.lower() for token in tokens]

    if not file_path:
        print(f"Article {article_num}: writing to file output/article{article_num}/3. Lowercased-output.txt")
        write_to_file(Path(f"article{article_num}/3. Lowercased-output.txt"), LOWER_CASED)
    else:
        print(f"Custom article: writing to file output/{file_path}")
        write_to_file(file_path, LOWER_CASED)

    return LOWER_CASED


if __name__ == '__main__':
    lowercaser()
