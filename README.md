# dbtAI

An AI CLI utility for common tasks with dbt. Commands are intended to run inside a dbt project, and parses the dbt manifest to provide relevant context for the LLM.

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
dbt unit <model_name> "<What to test>" [-w]
```

optionally write the test to the `<model_name>.yml` sidecar file with the `-w` or `--write` flag. When writing to file, `dbtai` assumes the file already exists (because you did write docs first, of course).


## Future work

### Generate code

Generate SQL code from a description. Maybe a command like

```bash
dbtai gen <model_name> "<Description of what to generate>"
```

### Fix code

Take the name of an existing model along with a description of what to change.

```bash
dbtai fix <model_name> "<Description of change>"
```

### Advanced fluffing

Take the name of an existing model, improve the SQL style by running sqlfluff (not LLM-related) and generating better column aliases, code comments, clean up logic etc.

```bash
dbtai fluff <model_name>
```


## That's all, folks!

Happy coding.