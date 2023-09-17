import rich
import typer
from typer import rich_utils
from rich.progress import Progress, TimeRemainingColumn, MofNCompleteColumn, TimeElapsedColumn, BarColumn

from utilities import textualize, get_all_texts
from tokenization import tokenize
from lowercase import lowercase
from stem import stem
from handle_stopwords import remove_stopwords

# Define certain colors and styles
rich_utils.OPTIONS_PANEL_TITLE = "[not dim]Options"

# Define Typer CLI app
app = typer.Typer(name="Reuters Data Pipeline", rich_markup_mode='rich', no_args_is_help=True,
                  add_completion=False)


@app.command(short_help="Run each step of the pipeline automatically.", options_metavar='[--help]',
             epilog="Thanks for using my data pipeline! :boom:", help="""
             Process the first 5 articles of the required Reuters corpus. Run each step of the pipeline automatically.
            
             [not dim]
             Runs the following functionality:\n
             1. Turn the given Reuters articles into a more standard textual format for easier processing
             2. Tokenize each article
             3. Lowercase each token for each article
             4. Stem each token for each article
             5. Remove stopwords for each article
             
             [bold yellow]Example Usage[/]:
             python Pipeline.py
             """)
def pipeline():
    """Run each step of the pipeline automatically"""

    # Create progress bar
    progress_bar = Progress('[progress.description]{task.description}', BarColumn(),
                            MofNCompleteColumn(), '|',
                            'Time Elapsed:', TimeElapsedColumn(),
                            'Estimated Time Remaining:', TimeRemainingColumn(compact=True)
                            )

    # Will need to print a statement indicating that articles beyond 5 won't be printed to the screen,
    # but only show this message once
    statement_printed = False

    # Get all the articles
    ALL_ARTICLES = get_all_texts()

    # Do all processing within the context of the progress bar, so it updates properly
    with progress_bar as progress:
        task = progress.add_task("Processing all articles...", total=len(ALL_ARTICLES))

        # Loop through each article and process it
        for i, article in enumerate(ALL_ARTICLES, start=1):

            # Only print detailed breakdowns for first 5 articles
            if i <= 5:
                rich.print(f"Article [bold green]{i}[/]:")
            else:
                if not statement_printed:
                    rich.print("\nArticles beyond [green bold]5[/] are processed, just not printed to the screen or saved to files\n")
                    statement_printed = True

            # Dome some helpful preprocessing to have text that can be saved to a file as initial text
            this_article = textualize(article, i)

            # Do normal pipeline steps, in order
            tokenized = tokenize(this_article, i, pipeline=True)
            lower_cased = lowercase(tokenized, i, pipeline=True)
            stemmed = stem(lower_cased, i, pipeline=True)
            _ = remove_stopwords(stemmed, i, pipeline=True)

            # Advance the progress bar
            progress.update(task, advance=1)


if __name__ == '__main__':
    app()
