import logging
import os

import openai

from Other.utils import read_file

openai.api_key = os.environ['OPENAI']
logger = logging.getLogger(__name__)

class LLM:
    def __init__(self, prompt: str) -> None:
        self.prompt = prompt

    def set_prompt(self, new_prompt):
        new_prompt = self.prompt

class OpenAILLM(LLM):
    def __init__(self,
                 prompt: str = None,
                 model: str = "gpt-5-mini",
                 messages: list = None,
                 temperature: float = 1.0,
                 stream: bool = True):
        super().__init__(prompt)
        self.model = model
        self.temperature = temperature
        self.stream = stream
        if messages is None:
            self.messages = []
        if self.prompt is not None:
            self.messages.append({"role": "assistant", "content": self.prompt})


    def set_prompt(self, prompt):
        self.messages[0]["content"] = prompt

    def generate_message(self, query: str):
        self.messages = [{"role": "assistant", "content": self.prompt}]
        self.messages.append({"role": "user", "content": query})
        response = openai.chat.completions.create(
            model=self.model,
            messages=self.messages,
            temperature=self.temperature,
            stream=self.stream
        )

        logging.info("Got a response!!!")
        if self.stream:
            message = self.stream_api_response(response)
        else:
            message = response.choices[0].message.content
        self.messages.append({"role": "assistant", "content": message})
        return message

    def stream_api_response(self, response):
        output = []
        temp = []
        for chunk in response:
            new_message = chunk.choices[0].delta.content
            if new_message:
                print(new_message, end='', flush=True)
                temp.append(new_message)
                if any(new_message.endswith(punct) for punct in ('.', '!', '?')):
                    temp_message = ''.join(temp)
                    output.append(''.join(temp))
                    temp = []
        if temp:
            temp_message = ''.join(temp)
        return ''.join(output)
def main():
    import pandas as pd
    prompt = read_file("../Data/prompts/clean_text.txt")
    llm = OpenAILLM(prompt=prompt, model="gpt-4o-mini", stream=False)

    df = pd.read_csv("../Data/CSV/produkty_hebe_raw.csv")

    def transform_one(x):
        if pd.isna(x) or str(x).strip() == "":
            return ""
        return llm.generate_message(str(x))

    print(llm.generate_message(df["skladniki"][0]))

    df.to_csv("../Data/produkty_hebe_transformed.csv", index=False)
if __name__ == '__main__':
    main()