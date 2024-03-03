import click
import inquirer
import appdirs
import json
import os
import yaml
from dbtai.templates.prompts import languages
from dbtai.manifest import Manifest

APPNAME = "dbtai"
APPAUTHOR = "dbtai"

@click.group()
def dbtai():
    pass


@dbtai.command(help="Generate documentation for a dbt model")
@click.argument('model', required=True)
@click.option('--write', '-w', is_flag=True, help='Write the generated documentation to file', default=False)
@click.option('--print', '-p', is_flag=True, help='Print the generated documentation', default=False)
def doc(model, write, print):
    manifest = Manifest()
    docs_json = manifest.generate_docs(model)
    docs_yaml = manifest.format_docs(docs_json)

    if write:
        doc_path = manifest.get_doc_location(model)
        with open(doc_path, "w") as f:
            f.write(docs_yaml)
    else:
        click.echo(docs_yaml)


@dbtai.command(help="Configure dbtai with preferred language, backend etc.")
def setup():

    language_choices = list(languages.keys())
    question = [
        inquirer.List('language',
                    message='What language would you like to use?',
                    choices=language_choices,
                    default='english'
                    ),
        inquirer.List('backend',
                        message ="LLM Backend",
                        choices = ["OpenAI", "Azure OpenAI"],
                        default = "OpenAI"
                        ),
        inquirer.List("auth_type",
                    message = "Authentication Type",
                    choices = ["API Key", "Native Authentication (DefaultAzureCredential)"],
                    default = "API Key",
                    ignore = lambda answers: answers['backend'] == "OpenAI"
                    ),
        inquirer.Text('api_key',
                    message='OpenAI API Key',
                    ignore = lambda answers: answers['auth_type'] == "Native Authentication (DefaultAzureCredential)"
                    ),
        inquirer.List("openai_model_name",
                    message = "Model Name",
                        choices = ["gpt-3.5-turbo", "gpt-4-turbo-preview"],
                    default = "gpt-4-turbo-preview",
                    ignore = lambda answers: answers['backend'] == "Azure OpenAI"
                    ),
        inquirer.Text("azure_endpoint",
                    message = "Azure OpenAI Endpoint",
                    ignore = lambda answers: answers['backend'] == "OpenAI"
                    ),
        inquirer.Text("azure_openai_model",
                    message = "Azure OpenAI Model",
                    ignore = lambda answers: answers['backend'] == "OpenAI"
                    ),
        inquirer.Text("azure_openai_deployment",
                    message = "Azure OpenAI Deployment",
                    ignore = lambda answers: answers['backend'] == "OpenAI"
                    ),
    ]
    answer = inquirer.prompt(question)

    # Save the configuration using appdirs
    configdir = appdirs.user_data_dir(APPNAME, APPAUTHOR)

    # Create the configuration directory if it doesn't exist
    os.makedirs(configdir, exist_ok=True)

    # Save the configuration to a file, using the YAML format. Replace if exists
    with open(os.path.join(configdir, "config.yaml"), "w") as f:
        yaml.dump(answer, f)

    click.echo(f"Configuration saved to {configdir}")


@dbtai.command(help="Show the current configuration")
def show():
    configdir = appdirs.user_data_dir(APPNAME, APPAUTHOR)

    with open(os.path.join(configdir, "config.yaml"), "r") as f:
        click.echo(f.read())


@dbtai.command(help="Create a dbt unit test for a given model")
@click.argument('model', required=True)
@click.argument('instructions', required=False)
@click.option('--write', '-w', is_flag=True, help='Write the generated test to file', default=False)
def unit(model, instructions, write):
    manifest = Manifest()
    test, explanation = manifest.generate_unittest(model, instructions)

    if write:
        doc_path = manifest.get_doc_location(model)
    # Append test to file, fail if file not exists
        with open(doc_path, "a") as f:
            f.write("\n\n")
            f.write(test)
    else:
        click.echo(test)
        click.echo(explanation)

@dbtai.command(help="Write dbt constraints given the uniqueness tests in the model")
def constraints():
    raise NotImplementedError("Not yet implemented")


@dbtai.command(help="Show logo")
def hello():
    greeting = r"""
    .______.    __       _____  .___ 
  __| _/\_ |___/  |_    /  _  \ |   |
 / __ |  | __ \   __\  /  /_\  \|   |
/ /_/ |  | \_\ \  |   /    |    \   |
\____ |  |___  /__|   \____|__  /___|
     \/      \/               \/     
"""
    click.echo(greeting)