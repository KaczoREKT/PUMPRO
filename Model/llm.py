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
                temp.append(new_message)
                if any(new_message.endswith(punct) for punct in ('.', '!', '?')):
                    temp_message = ''.join(temp)
                    output.append(''.join(temp))
                    temp = []
        if temp:
            temp_message = ''.join(temp)
        return ''.join(output)

if __name__ == '__main__':
    prompt = read_file('../Data/prompts/clean_text.txt')
    llm = OpenAILLM(prompt=prompt, model='gpt-5')
    string = '/Ingredients (INCI): Aqua, Lauryl Glucoside, Sodium Methyl Cocoyl Taurate, Sodium Cocoyl Isethionate, Disodium Lauryl Sulfosuccinate, Sodium Lauryl Glucose Carboxylate, Sodium Olivamphoacetate, Ceramide NP, Ceramide AP, Ceramide EOP, Ceramide NG, Olea Europaea (Olive) Fruit Oil, Withania Somnifera Root Extract, Ganoderma Lucidum Extract, Rhodiola Rosea Root Extract, Caffeine, Prunus Armeniaca (Apricot) Kernel Oil, Ricinus Communis (Castor) Seed Oil, Helianthus Annus Seed Oil, Tocopherol, Phytosphingosine, Cholesterol, Polyglyceryl-10 Stearate, Polyglyceryl-6 Behenate, Coco-Glucoside, Glycol Distearate, Cetearyl Alcohol, Glyceryl Stearate, Sodium Cetearyl Sulfate, Triethyl Citrate, Sodium Levulinate, Behenic Acid, Lysolecithin, Xantan Gum, Glycerin, Sodium Chloride, Citric Acid, Sodium Dehydroacetate, Potassium Sorbate, Sodium Benzoate, CI 15985, CI 16035, Parfum, Tetramethyl Acetyloctahydronaphthalenes, Citrus Aurantium Peel Oil, Linalool, Citronellol, Limonene.'
    print(llm.generate_message(string))