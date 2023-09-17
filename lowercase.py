from pathlib import Path
from typing import List, Optional
from typing_extensions import Annotated

import typer
from typer import rich_utils
import rich

from file_writing import write_to_file

# Define certain colors and styles
rich_utils.OPTIONS_PANEL_TITLE = "[not dim]Options"
rich_utils.ARGUMENTS_PANEL_TITLE = "[not dim]Arguments"
rich_utils.STYLE_REQUIRED_LONG = 'not dim red'
rich_utils.STYLE_OPTION_DEFAULT = 'not dim white'

# Define lowercaser app
lowercaser = typer.Typer(add_completion=False, rich_markup_mode='rich', no_args_is_help=True)

# Define certain app arguments and options. Makes later code cleaner
TOKENS_ARGUMENT = typer.Argument(help="The tokens to use, written as 1 or more space-separated strings.", show_default=False)
ARTICLE_NUM_OPTION = typer.Option(help="Which article in the corpus this is. Used in logging.", hidden=True)
FILE_OPTION = typer.Option("--file", "-f", help="Specify an optional file to save this result to.")


@lowercaser.command(short_help="Makes all tokens lowercase.", epilog="Thanks for using my token lower-caser! :boom:",
                    options_metavar='[--help] [--file <dir/file.txt>]', no_args_is_help=True,
                    help="""Makes all tokens lowercase.
                    
                    [not dim]
                    The arguments to this command are a list of tokens. These tokens are all made lowercase
                    
                    It is possible to specify a custom file to save results to. Files should always look like: [bold yellow]<nested/directories/file.txt>[/].
                    Regardless of the nesting of directories and filename you specify, results will always be saved to the [bold yellow]output/[/] directory.
                   
                    For instance, running: 
                   
                    python lowercase.py THESE ARE SOME TOKENS --file my_article/lowercase.txt
                   
                    will save to [bold yellow]output/my_article/lowercase.txt[/]. If no file is specified, it will save to
                    [bold yellow]output/custom_article/2. Lowercased-output.txt[/]
                   
                    [bold yellow]Example Usages[/]:
                    python lowercase.py THESE ARE SOME TOKENS
                    python lowercase.py THESE ARE SOME TOKENS --file my_article/lowercase.txt
                    """)
def lowercase(
        tokens: Annotated[List[str], TOKENS_ARGUMENT],
        article_num: Annotated[Optional[int], ARTICLE_NUM_OPTION] = 0,
        file_path: Annotated[Optional[Path], FILE_OPTION] = None,
        pipeline: Annotated[bool, typer.Option(hidden=True)] = False
) -> List[str]:
    """
    Turn the tokens of the article all lowercase

    :param tokens: The list of tokens to make lowercase
    :param article_num: Which article this is
    :param file_path: A file path to save the file to. Must take form of directory/file.txt
    :param pipeline: Whether this command is running as part of the pipeline. Changes file writing
    :return: The list of tokens, all lowercase
    """

    # Create the lowercase version of the input tokens list
    LOWER_CASED: List[str] = [token.lower() for token in tokens]

    # If this is running as the pipeline, this will be the 3rd file written
    if pipeline:
        file_print = Path(f"article{article_num}/3. Lowercased-output.txt")
        rich.print(f"\twriting to file \"{'output' / file_print}\"")
        write_to_file(file_print, LOWER_CASED)

    # If this is not running as the pipeline, this will be the 2nd file written
    else:
        # If a file is specified, write to it
        if file_path:
            rich.print(f"\nCustom article: writing to file \"{'output' / file_path}\"")
            write_to_file(file_path, LOWER_CASED)

        # If not, write to default location
        else:
            file_print = Path("custom_article/2. Lowercased-output.txt")
            rich.print(f"\nCustom article: writing to file \"{'output' / file_print}\"")
            write_to_file(file_print, LOWER_CASED)

        # When not in pipeline, print output to screen
        rich.print(f"\n[bold blue]Output:[/]\n{' '.join(t for t in LOWER_CASED)}")

    return LOWER_CASED


if __name__ == '__main__':
    lowercaser()
