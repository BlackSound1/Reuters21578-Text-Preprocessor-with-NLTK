# Reuters21578 Text Preprocessor with NLTK

## Installation
Download the Reuters 21578 corpus from http://www.daviddlewis.com/resources/testcollections/reuters21578/. Extract it to the same level as the project into a folder called `reuters21578`.

Install all dependencies in `requirements.txt`.

## Running
This is implemented as a Typer CLI app.

The commands available are:

  - `$ python Pipeline.py`: Run the whole pipeline.
  - `$ python tokenization.py`: Run only the tokenization step of the pipeline.
  - `$ python lowercase.py`: Run only the lower-caser step of the pipeline.
  - `$ python stem.py`: Run only the stemming step of the pipeline.
  - `$ python handle_stopwords.py`: Run only the stopword-removal step of the pipeline.

For any of these commands, use the `--help` flag to see a full in-app documentation screen with code examples and full descriptions.

## Shortcomings

  - Although the pipeline scripts, when run standalone, work in a similar way to when they’re
run in the pipeline, the experience is not exactly the same. For instance, the `textualize()`
function is only run from within the pipeline. So having clean input text is your responsibility
when using the tokenizer independently.

  - When running the tokenizer independently, note that it takes as a mandatory argument, the
article text to tokenize. Since this is inputted via the command line, it may misbehave if you
supply text that has line breaks in it. It is best to supply very small “articles” when running
the pipeline steps via the command line. Inputting large text for the tokenizer may be quite
tedious to do properly. 
