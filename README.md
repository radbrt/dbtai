# dbtAI

An AI CLI utility for common tasks with dbt. Commands are intended to run inside a dbt project, and parses the dbt manifest to provide relevant context for the LLM.

Features include:
- Generate documentation for an existing dbt model, based on the upstream models and the model code.
- Generate Unit tests for a dbt model, given a description of what to test.
- Explain a dbt model.
- Interactively chat with a dbt model.
- Run SQLFluff and optionally rewrite a model for clarity.
- Change an existing model based on a description of desired changes.

## Get started

The library currently only works with OpenAI as backend. We hope to expand this, but for now you need an OpenAI API key at hand.

### Install
Install the library with:

```bash
pip install git+https://github.com/radbrt/dbtai.git
```

### Configure

By default, `dbtai` uses english prompt templates and looks for an OS env variable `OPENAI_API_KEY`. You can, however, choose another language and set your API key explicitly by running

```bash
dbtai setup
```

Currently supported languages:
- English
- Chinese
- Norwegian
- Spanish (autotranslated)
- French (autotranslated)
- German


## Use

`dbtai` currently provides the following functionality

### Create model documentation

```bash
dbtai doc <model_name> [-w]
```

Generate documentation for a given model name, optionally write it to a `<model_name>.yml` sidecar file with the `-w` or `--write` flag.

`dbtai` is fairly opinionated in using sidecar files with a 1:1 relationship between model.sql and model.yml. Not only is this often a preferred pattern, it simplifies the CLI utility significantly.

### Create unit tests

`dbtai`can create unit tests for any model with the command 

```bash
dbtai unit <model_name> "<What to test>" [-w]
```

optionally write the test to the `<model_name>.yml` sidecar file with the `-w` or `--write` flag. When writing to file, `dbtai` assumes the file already exists (because you did write docs first, of course).


### Generate new models

Create a new model from a description and a list of inputs.

```bash
dbtai gen -i companies_model -i sales_model "Join the tables on company_id and aggregate sales"
```

`dbtai` collects relevant upstream information and prints the result to the terminal.


### Make changes to existing models

Give `dbtai` an existing model, describe the changes you want, and get a suggestion for the model code.

```bash
dbtai fix companies_model "create rolling median monthly sales for previous 12 months column"
```

Optionally view the diff between the existing and new suggestion by passing the `--diff` option (seems to be buggy).


### Advanced fluffing

Take the name of an existing model, improve the SQL style by running sqlfluff (not LLM-related) and generating better column aliases, code comments, clean up logic etc. Optionally use the `--rewrite` to have OpenAI rewrite the model code after fluffing.

```bash
dbtai fluff <model_name> [--rewrite] [--write]
```

Use `--write` to automatically overwrite the existing model file with the new linted version.

### Explain

Simply read a model and it's context to explain what the model actually does, and why.

```bash
dbtai explain <model_name>
```

### Chat
You can open an interactive chat with a dbt model:

```bash
dbtai chat <model_name>
```

This will open a CLI chat, letting you ask questions and get answers interactively, keeping the chat history.

Save the chat history to file by typing `\save` inside the chat. You can still continue the chat after saving.


## That's all, folks!

Happy coding.