"""
Chatbot that uses the OPENAI api
api key needs to be set at OPENAI_API_KEY environment variable
"""

import os
import openai
from dotenv import load_dotenv

class Chatbot:
    __api_key: str
    __model: str
    conversation: list

    def __init__(self) -> None:
        load_dotenv()
        self.__api_key = os.getenv('OPENAI_API_KEY')
        if(self.__api_key == None):
            print('Error: no API key provided, please set \'OPENAI_API_KEY\' environment variable')
            exit(0)
        self.conversation = []
    
    def set_model(self, model: str) -> None:
        self.__model = model
    
    def get_model(self) -> str:
        return self.__model

    def get_response(self, prompt: str) -> str:
        # append the prompt to the convo
        self.conversation.append({'role': 'user', 'content': prompt})

        # Make an API call to OpenAI with the conversation history
        print('\ncalling api ...\n')
        response = openai.ChatCompletion.create(
            model=self.__model,
            messages=self.conversation,
            temperature=0.9,
            n=1,
            stop=None,
        )
        try:
            # get answer message from response
            response_message: str = response.choices[0].message.content
        except:
            print('\nerror when calling api')
            exit(0)

        # Append the model response to the conversation and return
        self.conversation.append({'role': 'assistant', 'content': response_message})
        return response_message


