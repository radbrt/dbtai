import os
import json
from dbtai.templates.prompts import (
    languages, 
    UNITTEST, 
    GENERATE_MODEL, 
    GENERATE_MODEL_SYSTEM_PROMPT, 
    FIX_MODEL_PROMPT,
    FIX_CODE_PROMPT
)
import appdirs
import yaml
from openai import OpenAI
from mistralai.client import MistralClient
from ruamel.yaml import YAML
from ruamel.yaml.comments import CommentedMap
import io
import difflib
import sqlfluff

class Manifest():

    def __init__(
        self,
        manifest_path = 'target/manifest.json'
    ):
        """Initialize the manifest object by loading the manifest, the user config and the OpenAI client.
        
        Args:
            manifest_path (str, optional): The path to the manifest. Defaults to 'target/manifest.json'.
        """
        self.manifest_path = manifest_path

        if not os.path.exists('dbt_project.yml'):
            raise FileNotFoundError(f"dbt_project.yml not found. Are you in the dbt directory?")

        if not os.path.exists(self.manifest_path):
            raise FileNotFoundError(f"dbt manifest not found. Have you run a dbt command such as `dbt run` or `dbt compile`?")
        
        with open(self.manifest_path, 'r') as file:
            self.manifest = json.load(file)

        self.config = self._load_config()
        if self.config['backend'] == "Mistral":
            self.client = self._make_mistral_client()
        elif self.config['backend'] == "Azure OpenAI":
            raise NotImplementedError("Azure OpenAI not yet implemented")
        else:
            self.client = self._make_openai_client()
    def _make_openai_client(self):
        """Make the OpenAI client with auth."""

        if self.config['backend'] == "OpenAI":
            api_key = self.config['api_key'] or os.getenv("OPENAI_API_KEY")
            return OpenAI(api_key=api_key)
        else:
            raise NotImplementedError("Azure OpenAI not yet implemented")

    def _make_mistral_client(self):
        """Make the Mistral client with auth."""
        client = MistralClient(api_key=self.config['api_key'])
        return client


    def chat_completion(self, messages, response_format_type="json_object"):
        """Convenience method to call the chat completion endpoint.
        
        Args:
            messages (list): A list of messages to send to the chat API
            response_format_type (str, optional): The response format. Defaults to "json_object".

        Returns:
            openai.ChatCompletion: The response from the chat API
        """
        if self.config["backend"] == "OpenAI":
            if not self.config.get("openai_model_name"):
                raise ValueError("OpenAI model name not set in config")

            return self.client.chat.completions.create(
                model=self.config.get('openai_model_name', 'gpt-4-turbo-preview'), 
                messages=messages,
                response_format={"type": response_format_type}
            )
        elif self.config["backend"] == "Mistral":

            return self.client.chat(
                model=self.config.get("mistral_model_name", "mistral-large-latest"),
                messages=messages,
                response_format={"type": response_format_type},
            )

        else:
            raise NotImplementedError("Your backend is set to Azure OpenAI not yet implemented")

    def _load_config(self):
        """Convenience function to load the user config from the config file."""
        configdir = appdirs.user_data_dir("dbtai", "dbtai")

        if os.path.exists(os.path.join(configdir, "config.yaml")):
            with open(os.path.join(configdir, "config.yaml"), "r") as f:
                return yaml.load(f, Loader=yaml.FullLoader)

        return {'language': 'english', "backend": "OpenAI"}


    def get_nodes_and_sources(self):
        """Get the nodes and sources from the manifest."""
        return {**self.manifest['nodes'], **self.manifest['sources']}


    def get_model_from_name(self, model_name):
        """Get the model from the manifest.
        
        Args:
            model_name (str): The name of the model.
            
        Returns:
            dict: The model from the manifest.
        """
        nodes_and_sources = self.get_nodes_and_sources()
        for id, model in nodes_and_sources.items():
            if model['name'] == model_name:
                return model
        raise ValueError(f"Model {model_name} not found in the manifest")


    def get_upstream_models(self, model_name):
        """Get the upstream models of a model.
        
        Args:
            model_name (str): The name of the model.

        Returns:
            list[dict]: A list of upstream models (dictionaries).
        """
        model = self.get_model_from_name(model_name)
        nodes_and_sources = self.get_nodes_and_sources()

        if model:
            upstrea_models = [nodes_and_sources[model_id] for model_id in model['depends_on']['nodes']]
            return upstrea_models
        return []


    def compile_upstream_description_markdown(self, model_name):
        """Compile the documentation for upstream models into a markdown string.
        
        Args:
            model_name (str): The name of the model to get upstream documentation for.

        Returns:
            str: A markdown string with the documentation for all upstream models.
        """
        upstream_models = self.get_upstream_models(model_name)

        all_models = []
        if upstream_models:
            for model in upstream_models:
                top_level_description = f'{model["name"]}: {model.get("description") or "(no description)"}'
                column_descriptions = '\n'.join(
                    [f'* {column}: {content.get("description") or "(no description)"}' 
                    for column, content in model['columns'].items()]
                    ) or '(no columns defined)'
                all_models.append(f'{top_level_description}\nColumns:\n{column_descriptions}')
        return '\n\n'.join(all_models)


    def get_model_description(self, model_name):
        """Get the description of a model.
        
        Args:
            model_name (str): The name of the model.

        Returns:
            str: The description of the model.
        """
        model = self.get_model_from_name(model_name)

        top_level_description = model.get('description') or "(no description)"
        column_descriptions = '\n'.join(
        [f'* {column}: {content.get("description") or "(no description)"}' 
        for column, content in model['columns'].items()]
        ) or '(no columns defined)'

        return f'{top_level_description}\nColumns:\n{column_descriptions}'


    def create_documentation_instructions(self, model_name):
        """Create a markdown prompt with instructions for documenting the model.
        
        Args:
            model_name (str): The name of the model to create instructions for.
            
        Returns:
            str: A markdown string with instructions for the model.
        """
        model_description = self.compile_upstream_description_markdown(model_name)

        raw_code = self.get_model_from_name(model_name)['raw_code']

        REQUEST = languages[self.config['language']]['create_docs_prompt']

        return REQUEST.format(
            model_description=model_description, 
            raw_code=raw_code, 
            model_name=model_name)

    def make_unittest_query(self, model_name, extra_instructions=''):

        raw_code = self.get_model_from_name(model_name)['raw_code']
        model_description = self.compile_upstream_description_markdown(model_name)

        frm = UNITTEST.format(
            model_name=model_name,
            raw_code=raw_code,
            model_description=model_description,
            extra_instructions=extra_instructions or ' '
        )

        return frm

    def generate_unittest(self, model_name, extra_instructions=None):
        """Generate a unit test for the model."""
        updoc = self.make_unittest_query(model_name, extra_instructions)
        prompt = languages[self.config['language']]['system_prompt']

        response = self.chat_completion(
            messages=[
                {"role": "system", "content":prompt},
                {"role": "user", "content": updoc}
            ]
        )

        response_json = json.loads(response.choices[0].message.model_dump_json())
        test_json = json.loads(response_json['content'])
        return test_json['unit_test'], test_json["explanation"]

    def generate_docs(self, model_name):
        """Generate documentation for the model."""
        updoc = self.create_documentation_instructions(model_name)
        prompt = languages[self.config['language']]['system_prompt']

        response = self.chat_completion(
            messages=[
                {"role": "system", "content":prompt},
                {"role": "user", "content": updoc}
            ]
        )

        response_json = json.loads(response.choices[0].message.model_dump_json())
        docs_json = json.loads(response_json['content'])
        return docs_json

    def get_model_location(self, model_name):
        """Get the file location of the model.
        
        Args:
            model_name (str): The name of the model.
            
        Returns:
            str: The file location of the model.
        """
        model = self.get_model_from_name(model_name)
        return model['original_file_path']

    def get_doc_location(self, model_name):
        """Get the file location of the documentation for the model.
        By design, this is just a sidecar to the model file.

        Args:
            model_name (str): The name of the model.

        Returns:
            str: The file location of the documentation for the model.
        """
        model = self.get_model_from_name(model_name)
        return model['original_file_path'].replace('.sql', '.yml')
    
    @staticmethod
    def format_docs(docs_json):
        """Format the documentation into a markdown string.
        
        Args:
            docs_json (dict): The documentation in JSON format.

        Returns:
            str: The documentation in markdown format, correctly ordered.
        """

        ordered_data = CommentedMap()
        ordered_data['name'] = docs_json['name']
        ordered_data['description'] = docs_json['description']
        ordered_data['columns'] = docs_json['columns']

        full_data = CommentedMap()
        full_data['version'] = 2
        full_data['models'] = [ordered_data]

        yaml = YAML()
        yaml.indent(sequence=4, offset=2)
        yaml.preserve_quotes = True
        output_stream = io.StringIO()
        yaml.dump(full_data, output_stream)
        yaml_string = output_stream.getvalue()
        output_stream.close()

        return yaml_string


    def generate_model(self, model_name, description, inputs=[]):
        """Generate model from a description and inputs.
        
        Args:
            model_name (str): The name of the model.
            description (str): The description of the model.
            inputs (list, optional): A list of upstream models. Defaults to [].

        Returns:
            dict: The generated model in JSON format with keys "code" and "explanation".
        """

        if len(inputs) > 0:
            inputs = [self.compile_upstream_description_markdown(model_name) for model_name in inputs]
            upstream_docs = '\n\n'.join(inputs)
        else:
            upstream_docs = None
        
        prompt = GENERATE_MODEL.format(
            model_name=model_name,
            description=description,
            upstream_docs=upstream_docs
        )

        response = self.chat_completion(
            messages=[
                {"role": "system", "content": GENERATE_MODEL_SYSTEM_PROMPT},
                {"role": "user", "content":prompt}
            ]
        )

        response_json = json.loads(response.choices[0].message.model_dump_json())
        docs_json = json.loads(response_json['content'])
        return docs_json
    
    def fix(self, model_name, description):
        """Make a change to a model, based on a description of the issue.
        
        Args:
            model_name (str): The name of the model.
            description (str): The description of the issue.

        Returns:
            dict: The fixed model in JSON format with keys "code" and "explanation".
        """
        upstream_docs = self.compile_upstream_description_markdown(model_name)

        model_code = self.get_model_from_name(model_name)['raw_code']

        prompt = FIX_MODEL_PROMPT.format(
            model_code=model_code,
            issue = description,
            tables = upstream_docs
        )

        response = self.chat_completion(
            messages=[
                {"role": "system", "content": GENERATE_MODEL_SYSTEM_PROMPT},
                {"role": "user", "content":prompt}
            ]
        )

        response_json = json.loads(response.choices[0].message.model_dump_json())
        docs_json = json.loads(response_json['content'])

        new_code = docs_json['code']
        diff = difflib.unified_diff(model_code, new_code, fromfile='model_code', tofile='new_code')
        docs_json['diff'] = diff

        return docs_json
    
    def fluff(self, model_name, rewrite=True):
        model_code = self.get_model_from_name(model_name)['raw_code']

        linted_code = sqlfluff.fix(model_code)

        prompt = FIX_CODE_PROMPT.format(
            model_code=linted_code
        )

        if not rewrite:
            return {"code": linted_code, "explanation": "SQLFluffed code, no rewrite"}

        response = self.chat_completion(
            messages=[
                {"role": "system", "content":prompt}
            ]
        )

        response_json = json.loads(response.choices[0].message.model_dump_json())
        docs_json = json.loads(response_json['content'])

        return docs_json
    
    def explain(self, model_name):
        model_code = self.get_model_from_name(model_name)['raw_code']
        upstream_docs = self.compile_upstream_description_markdown(model_name)
        model_docs = self.compile_upstream_description_markdown(model_name)

        prompt = languages[self.config['language']]['explain_prompt'].format(
            raw_code=model_code,
            upstream_models=upstream_docs,
            model_name=model_name,
            model_description=model_docs
        )

        response = self.chat_completion(
            messages=[
                {"role": "system", "content": languages[self.config['language']]['explain_system_prompt']},
                {"role": "user", "content": prompt}
            ],
            response_format_type="text"
        )

        return response.choices[0].message.content
    
    def generate_chatbot_prompt(self, model):
        model_docs = self.get_model_description(model)
        upstream_docs = self.compile_upstream_description_markdown(model)
        model_code = self.get_model_from_name(model)['raw_code']
        prompt = languages[self.config['language']]['chatbot_prompt'].format(
            model_name=model,
            raw_code=model_code,
            upstream_models = upstream_docs,
            model_description=model_docs
        )
        return prompt