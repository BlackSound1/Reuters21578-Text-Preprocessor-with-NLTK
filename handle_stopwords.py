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

remover = typer.Typer(name="Stopword-Remover", short_help="A Module for removing stopwords from a list of tokens.",
                      add_completion=False, rich_markup_mode='rich', no_args_is_help=True)


@remover.command(name='remove_stopwords', short_help="Removes stopwords from a given list of tokens.",
                 rich_help_panel='COMMANDS', options_metavar='[--help]', no_args_is_help=True,
                 epilog="Thanks for using my stopwords-remover! :boom:",
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
                   
                 python lowercase.py where are you at for once --file-path my_article/removed.txt
                   
                 will save to [bold yellow]output/my_article/removed.txt[/]
                 
                 [bold yellow]Example Usages[/]:
                 python handle_stopwords.py where are you at for once
                 python handle_stopwords.py these are other tokens perhaps with stopwords --stopwords-file my_file.txt
                 python handle_stopwords.py where are you at for once --file-path my_article/removed.txt
                 python handle_stopwords.py where are you at for once --file-path my_article/removed.txt --stopwords-file my_file.txt
                 """)
def remove_stopwords(
        tokens: Annotated[List[str], typer.Argument(help="The tokens to use.", show_default=False)],
        article_num: Annotated[Optional[int], typer.Option(help="Declare which article number this should be.",
                                                           hidden=True)] = 0,
        stopwords_file: Annotated[Optional[Path], typer.Option(help="The file to find stopwords in.")] = Path(
            "Stopwords-used-for-output.txt"),
        file_path: Annotated[Path, typer.Option(help="Specify an optional file to save this result to.")] = Path(
            'custom_article/4. No-stopword-output.txt')

) -> None:
    """
    As the final step, remove all words from the list of tokens that are stopwords

    :param tokens: The list of tokens to filter stopwords out of
    :param article_num: Which article this is
    :param stopwords_file: The file where stopwords are defined
    :param file_path: A file path to save the file to. Must take form of directory/file.txt
    """

    # Read the given stopwords file and create a list of the stopwords within
    with open(stopwords_file, "r") as file:
        STOPWORDS: List[str] = [word.strip() for word in file.readlines()]

    # Filter out the stopwords
    FINAL: List[str] = [word for word in tokens if word not in STOPWORDS]

    if not file_path:
        print(f"Article {article_num}: writing to file output/article{article_num}/5. No-stopword-output.txt")
        write_to_file(Path(f"article{article_num}/5. No-stopword-output.txt"), FINAL)
    else:
        print(f"Custom article: writing to file output/{file_path}")
        write_to_file(file_path, FINAL)


if __name__ == '__main__':
    remover()
