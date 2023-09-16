from pathlib import Path

import typer
from typer import rich_utils

from utilities import get_five_articles, textualize
from tokenization import tokenize
from lowercase import lowercase
from stem import stem
from handle_stopwords import remove_stopwords


# Define certain colors and styles
rich_utils.OPTIONS_PANEL_TITLE = "[not dim]Options"

# Define Typer CLI app
app = typer.Typer(name="Reuters Data Pipeline", rich_markup_mode='rich', no_args_is_help=True,
                  add_completion=False)


@app.command(name="pipeline", short_help="Run each step of the pipeline automatically.",
             options_metavar='[--help]', epilog="Thanks for using my data pipeline! :boom:",  help="""
             Process the first 5 articles of the required Reuters corpus. Run each step of the pipeline automatically.
            
             [not dim]
             Runs the following functionality:\n
             1. Turn the given Reuters articles into a more standard textual format for easier processing
             2. Tokenize each article
             3. Lowercase each token for each article
             4. Stem each token for each article
             5. Remove stopwords for each article
             """)
def pipeline():
    """Run each step of the pipeline automatically"""

    ALL_ARTICLES = get_five_articles()
    STOPWORDS_FILE = Path("Stopwords-used-for-output.txt")

    for i, article in enumerate(ALL_ARTICLES, start=1):
        this_article = textualize(article, i)
        tokenized = tokenize(this_article, i)
        lower_cased = lowercase(tokenized, i)
        stemmed = stem(lower_cased, i)
        remove_stopwords(stemmed, i, STOPWORDS_FILE)


if __name__ == '__main__':
    app()
