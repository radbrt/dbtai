import openai
import os
import appdirs
import yaml
import click
import datetime

class ModelChatBot:
    def __init__(
            self,
            model_name,
            system_prompt
        ):

        self.config = self._load_config()
        self.model_name = model_name
        self.chat_history = [
            {"role": "system", "content": system_prompt}
        ]

        self.client = openai.OpenAI(api_key=self.config["api_key"] or os.getenv("OPENAI_API_KEY"))

    def _load_config(self):
        """Convenience function to load the user config from the config file."""
        configdir = appdirs.user_data_dir("dbtai", "dbtai")

        if os.path.exists(os.path.join(configdir, "config.yaml")):
            with open(os.path.join(configdir, "config.yaml"), "r") as f:
                return yaml.load(f, Loader=yaml.FullLoader)

        return {'language': 'english', "backend": "OpenAI"}

    def chat_completion(self, messages):
        """Convenience method to call the chat completion endpoint.
        
        Args:
            messages (list): A list of messages to send to the chat API
            response_format_type (str, optional): The response format. Defaults to "json_object".

        Returns:
            openai.ChatCompletion: The response from the chat API
        """
        if self.config["backend"] == "OpenAI":
            return self.client.chat.completions.create(
                model=self.config["openai_model_name"], 
                messages=messages
            )
        else:
            return self.client.chat.completions.create(
                model=self.config["azure_openai_model"], 
                messages=messages,
                deployment=self.config["azure_openai_deployment"],
                endpoint=self.config["azure_endpoint"]
            )


    def run(self):
        print(f"""
Hi! I'm here to chat about the dbt model {self.model_name}. What's on your mind?
Type 'quit' or hit Ctrl-C to exit)
        """
        )
        while True:
            user_input = input(">>> ")
            if user_input.lower() in ['quit', 'exit']:
                print("Goodbye!")
                break

            if user_input == r"\save":
                with open('chat_history.txt', 'a') as f:
                    f.write(f"Chat history for the dbt model: {self.model_name}, on {datetime.datetime.now().isoformat()}\n\n")
                    for item in self.chat_history:
                        f.write("%s\n" % item)
                click.echo(click.style(response.choices[0].message.content, fg='blue'))
                print("Chat history saved to chat_history.txt")
                continue

            self.chat_history.append({"role": "user", "content": user_input})
            response = self.chat_completion(self.chat_history)
            click.echo(click.style(response.choices[0].message.content, fg='blue'))
            self.chat_history.append({"role": "system", "content": response.choices[0].message.content})
