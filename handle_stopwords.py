from typing import List, Optional
from pathlib import Path

from typer import rich_utils
from typing_extensions import Annotated

import typer

from file_writing import write_to_file

# Define certain colors and styles
rich_utils.OPTIONS_PANEL_TITLE = "[not dim]Options"
rich_utils.ARGUMENTS_PANEL_TITLE = "[not dim]Arguments"
rich_utils.STYLE_REQUIRED_LONG = 'not dim red'
rich_utils.STYLE_OPTION_DEFAULT = 'not dim white'

# Define remover app
remover = typer.Typer(add_completion=False, rich_markup_mode='rich', no_args_is_help=True)

# Define certain app arguments and options. Makes later code cleaner
TOKENS_ARGUMENT = typer.Argument(help="The tokens to use.", show_default=False)
ARTICLE_NUM_OPTION = typer.Option(help="Declare which article number this should be.", hidden=True)
STOPWORDS_OPTION = typer.Option('--stopwords', "-s", help="The file to find stopwords in.")
FILE_OPTION = typer.Option("--file", "-f", help="Specify an optional file to save this result to.")


@remover.command(short_help="Removes stopwords from a given list of tokens.", no_args_is_help=True,
                 options_metavar='[--help] [--file <dir/file.txt>]', epilog="Thanks for using my stopwords-remover! :boom:",
                 help="""
                 Removes stopwords from a given list of tokens.
                 
                 [not dim]
                 Stopwords are extremely common words that can perhaps be ignored when doing NLP tasks, because they
                 don't differentiate texts from each other. This command reads a file of stopwords to eliminate from
                 a given list of token strings, and eliminates them. It's even possible to specify a custom stopwords
                 file.
                 
                 It is possible to specify a custom file to save results to. Files should always look like: [bold yellow]<nested/directories/file.txt>[/].
                 Regardless of the nesting of directories and filename you specify, results will always be saved to the [bold yellow]output/[/] directory.
                   
                 For instance, running: 
                   
                 python lowercase.py where are you at for once --file my_article/removed.txt
                   
                 will save to [bold yellow]output/my_article/removed.txt[/]. If no file is specified, it will save to
                 [bold yellow]output/custom_article/4. No-stopword-output.txt[/]
                 
                 [bold yellow]Example Usages[/]:
                 python handle_stopwords.py where are you at for once
                 python handle_stopwords.py these are other tokens perhaps with stopwords --stopwords my_file.txt
                 python handle_stopwords.py where are you at for once --file my_article/removed.txt
                 python handle_stopwords.py where are you at for once --file my_article/removed.txt --stopwords my_file.txt
                 """)
def remove_stopwords(
        tokens: Annotated[List[str], TOKENS_ARGUMENT],
        article_num: Annotated[Optional[int], ARTICLE_NUM_OPTION] = 0,
        stopwords_file: Annotated[Optional[Path], STOPWORDS_OPTION] = Path("Stopwords-used-for-output.txt"),
        file_path: Annotated[Optional[Path], FILE_OPTION] = None,
        pipeline: Annotated[bool, typer.Option(hidden=True)] = False
) -> None:
    """
    As the final step, remove all words from the list of tokens that are stopwords

    :param tokens: The list of tokens to filter stopwords out of
    :param article_num: Which article this is
    :param stopwords_file: The file where stopwords are defined
    :param pipeline: Whether this command is running as part of the pipeline. Changes file writing
    :param file_path: A file path to save the file to. Must take form of directory/file.txt
    """

    # Read the given stopwords file and create a list of the stopwords within
    with open(stopwords_file, "r") as file:
        STOPWORDS: List[str] = [word.strip() for word in file.readlines()]

    # Filter out the stopwords
    FINAL: List[str] = [word for word in tokens if word not in STOPWORDS]

    # If this is running as the pipeline, this will be the 5th file written
    if pipeline:
        print(f"Article {article_num}: writing to file output/article{article_num}/5. No-stopword-output.txt")
        write_to_file(Path(f"article{article_num}/5. No-stopword-output.txt"), FINAL)

    # If this is not running as the pipeline, this will be the 4th file written
    else:
        # If a file is specified, write to it
        if file_path:
            print(f"Custom article: writing to file output/{file_path}")
            write_to_file(file_path, FINAL)

        # If not, write to default location
        else:
            print("Custom article: writing to file output/custom_article/4. No-stopword-output.txt")
            write_to_file(Path("custom_article/4. No-stopword-output.txt"), FINAL)


if __name__ == '__main__':
    remover()
