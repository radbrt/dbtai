import click
import inquirer
import appdirs
import json
import os
import yaml
from dbtai.templates.prompts import languages, GENERATE_MODEL
from dbtai.manifest import Manifest
from dbtai.chatbot import ModelChatBot

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
    """Generate documentation for a dbt model.
    
    Args:
        model (str): The name of the dbt model
        write (bool): Write the generated documentation to file
        print (bool): Print the generated documentation
    """
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

@dbtai.command(help="Not yet implemented. Write dbt constraints given the uniqueness tests in the model")
def constraints():
    raise NotImplementedError("Not yet implemented")


@dbtai.command(help="Generate model code")
@click.argument("model_name", required=True)
@click.argument("description", required=True)
@click.option("--input", "-i", required=False, help="Name of Input model. Can be passed multiple times to reference several models", multiple=True)
def gen(model_name, description, input):
    manifest = Manifest()
    model = manifest.generate_model(model_name, description, input)
    click.echo(model["code"])
    click.echo(f"\n\n{model['explanation']}")


@dbtai.command(help="Make a change to a dbt model")
@click.argument("model_name", required=True)
@click.argument("description", required=True)
@click.option("--diff", "-d", is_flag=True, help="Show the diff between existing and suggested code", default=False)
def fix(model_name, description, diff):
    manifest = Manifest()
    click.echo(model_name)
    click.echo(description)

    model = manifest.fix(model_name, description)

    if diff:
        for line in model['diff']:
            print(line)
            if line.startswith('+'):
                click.echo(click.style(line, fg='green'))
            elif line.startswith('-'):
                click.echo(click.style(line, fg='red'))
    else:
        click.echo(model["code"])
        click.echo(f"\n\n{model['explanation']}")


@dbtai.command(help="Fluff the code")
@click.argument("model", required=True)
@click.option("--write", "-w", is_flag=True, help="Write the fluffed code to file", default=False)
@click.option("--rewrite", is_flag=True, help="Write the fluffed code to file and overwrite the original", default=False)
def fluff(model, write, rewrite):
    manifest = Manifest()
    result = manifest.fluff(model, rewrite=rewrite)

    if not write:
        click.echo(result['code'])
    else:
        write_path = manifest.get_model_location(model)
        with open(write_path, "w") as f:
            f.write(result['code'])


@dbtai.command(help="Explain the dbt code")
@click.argument("model", required=True)
def explain(model):
    manifest = Manifest()
    result = manifest.explain(model)
    click.echo(result)


@dbtai.command(help="Chat with a dbt model")
@click.argument("model", required=True)
def chat(model):
    manifest = Manifest()
    chatbot_prompt = manifest.generate_chatbot_prompt(model)
    chatbot = ModelChatBot(
        model_name=model,
        system_prompt=chatbot_prompt
    )
    chatbot.run()



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