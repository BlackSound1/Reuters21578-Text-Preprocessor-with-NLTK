from typing import Annotated

import rich
import typer
from typer import rich_utils
from rich.progress import Progress, TimeRemainingColumn, MofNCompleteColumn, TimeElapsedColumn, BarColumn

from utilities import textualize, get_texts, count_callback
from tokenization import tokenize
from lowercase import lowercase
from stem import stem
from handle_stopwords import remove_stopwords

# Define certain colors and styles
rich_utils.OPTIONS_PANEL_TITLE = "[not dim]Options"

# Define Typer CLI app
app = typer.Typer(name="Reuters Data Pipeline", rich_markup_mode='rich', no_args_is_help=True,
                  add_completion=False)

# Define certain app arguments and options. Makes later code cleaner
ARTICLE_COUNT_OPTION = typer.Option(hidden=True, callback=count_callback,
                                    prompt="\nPlease select how many articles to process and create output files for "
                                           "[\"all\" | any number >= 1]",
                                    help="If --all is not selected, how many articles to process and create output "
                                         "files for.")


@app.command(options_metavar='[--help]', epilog="Thanks for using my data pipeline! :boom:",
             help="""Process requested number of articles of the required Reuters corpus.
             Run each step of the pipeline automatically.
            
             [not dim]
             Upon running, a prompt will display asking how many articles in the corpus to process and create output
             files for. The default is "all". Enter any number >= 1 or "all".
             
             Runs the following functionality:\n
             1. Turn the given Reuters articles into a more standard textual format for easier processing
             2. Tokenize each article
             3. Lowercase each token for each article
             4. Stem each token for each article
             5. Remove stopwords for each article
             
             [bold yellow]Example Usage[/]:
             python Pipeline.py
             """)
def pipeline(article_count: Annotated[str, ARTICLE_COUNT_OPTION] = 'all') -> None:
    """Run each step of the pipeline automatically"""

    # Create progress bar
    progress_bar = Progress('[progress.description]{task.description}', BarColumn(),
                            MofNCompleteColumn(), '|',
                            'Time Elapsed:', TimeElapsedColumn(), '|',
                            'Estimated Time Remaining:', TimeRemainingColumn(compact=True)
                            )

    # Will need to print a statement indicating that articles beyond 5 won't be printed to the screen,
    # but only show this message once
    statement_printed = False

    # Determine if we're using all articles
    USING_ALL_ARTICLES = article_count.isalpha() and article_count.lower() == 'all'

    # Get all requested articles
    ALL_ARTICLES = get_texts(article_count=article_count)

    # Do all processing within the context of the progress bar, so it updates properly
    with progress_bar as progress:
        task = progress.add_task("Processing all articles...", total=len(ALL_ARTICLES))

        # Loop through each article and process it
        for i, article in enumerate(ALL_ARTICLES, start=1):

            # Only print detailed breakdowns for first 5 articles
            if i <= 5:
                rich.print(f"Article [bold green]{i}[/]:")
            else:
                if USING_ALL_ARTICLES or (article_count.isnumeric() and i > 5):
                    if not statement_printed:
                        rich.print("\nArticles beyond article [green bold]5[/] will be processed as well, "
                                   "and have their results saved to files. The details just won't be printed to the "
                                   "screen to avoid overwhelming the user\n")
                        statement_printed = True

            # Dome some helpful preprocessing to have text that can be saved to a file as initial text
            this_article = textualize(article, i)

            # Do normal pipeline steps, in order
            tokenized = tokenize(this_article, i, pipeline=True)
            lower_cased = lowercase(tokenized, i, pipeline=True)
            stemmed = stem(lower_cased, i, pipeline=True)
            _ = remove_stopwords(stemmed, i, pipeline=True)

            # For formatting
            if i == len(ALL_ARTICLES) and len(ALL_ARTICLES) <= 5:
                print()

            # Advance the progress bar
            progress.update(task, advance=1)

    rich.print("\n[bold green]DONE![/] Thanks for using my data pipeline! :boom:")


if __name__ == '__main__':
    app()
