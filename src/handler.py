"""
Handler module

This module contains the Handler class which is responsible for handling the conversation with the chatbot. 
It also contains the main function that starts the conversation.
"""
import getopt
import sys

from tkinter.filedialog import askopenfilename, asksaveasfilename
from api import Chatbot
from printing import print_instructions, print_response_formatted, print_usage

class Handler():
    chatbot: Chatbot
    prompt_actions: dict
    current_prompt: str
    __passed_prompt: bool
    headless_mode: bool = False
    default_model: str = 'gpt-3.5-turbo-0125'

    def __init__(self, headless: bool = False) -> None:
        chatbot: Chatbot = Chatbot()
        chatbot.set_model(self.default_model)
        self.chatbot = chatbot
        self.current_prompt = ''
        self.headless_mode = headless
        self.__passed_prompt = False
        self.prompt_actions = {
            'exit': lambda: sys.exit(0),
            'usage': self.handle_usage,
            'save': self.handle_save,
            'read': self.handle_read,
            '': lambda: None
        }

    def handle_usage(self) -> None:
        # clear prompt and print instructions
        self.current_prompt = ''
        print_instructions()

    def handle_save(self) -> None:
        # clear prompt
        self.current_prompt = ''

        file_path: str = asksaveasfilename(defaultextension='.md', filetypes=[('Text Files', '*.txt'), ('All Files', '*.*')]) if not self.headless_mode else input('Enter file name: ')
        file_path = file_path if file_path.endswith('.md') else file_path + '.md'

        try:
            with open(file_path, 'w') as file:
                # Iterate over list and write each item
                for message in self.chatbot.conversation:
                    file.write(f"**{message['role']}:**\n{message['content']}\n\n---\n")
            print(f'\nwriting conversation to: {file_path}')
            file.close()
        except Exception as e:
            print(f'\nAn error occurred while writing the file: {str(e)}')
    
    def handle_read(self, file_path: str = None) -> None:
        # clear prompt
        if not self.__passed_prompt:
            self.current_prompt = ''

        if file_path == None:
            file_path = askopenfilename(defaultextension='.txt', filetypes=[('Text Files', '*.txt'), ('All Files', '*.*')]) if not self.headless_mode else input('Enter relative path: ')

        try:
            with open(file_path, 'r') as file:
                self.current_prompt += file.read()
            print(f'\nreading following file: {file_path}')
        except FileNotFoundError:
            print('\nFile not found.')
        except Exception as e:
            print(f'\nAn error occurred while reading the file: {str(e)}')


    def handle_prompt(self) -> None:
        action = self.prompt_actions.get(self.current_prompt)
        if action:
            action()
        else:
            response: str = self.chatbot.get_response(self.current_prompt)
            print_response_formatted(response)
            self.current_prompt = ''
    
    def parse_options(self, argv: list) -> None:
        short_options: str = 'hr:p:m:'
        long_options: list = ['help', 'read=', 'prompt=', 'model=']

        # parse the command-line arguments
        arguments, values = getopt.getopt(argv[1:], short_options, long_options)

        # process arguments
        for current_argument, current_value in arguments:
            if current_argument in ('-r', '--read'):
                self.handle_read(current_value)

            elif current_argument in ('-p', '--prompt'):
                self.current_prompt += current_value
                print(f'\nhandling following prompt: {current_value}')
                self.__passed_prompt = True

            elif current_argument in ('-m', '--model'):
                model = 'gpt-4-turbo-preview' if current_value == '4' else self.default_model
                self.chatbot.set_model(model)
            
            elif current_argument in ('-h', '--help'):
                print(f'Usage: {argv[0]} [options...]')
                print_usage()
                sys.exit(0)

        
        # treat remaining arguments as prompt and append it to the prompt
        self.current_prompt += ' '.join(values)

    def convo(self, argv: list) -> None:
        self.parse_options(argv)
        print_instructions()
        print(f"\nmodel: {self.chatbot.get_model()}")
        
        if self.__passed_prompt:
            self.__passed_prompt = False
            self.handle_prompt()
    
        # main converstion loop
        while True:
            try:
                prompt = input('\nprompt: ')
                self.current_prompt += prompt
                self.handle_prompt()
            except SystemExit:
                break
            except Exception as e:
                print(f'\nError: {e}')
                print('\ncontinue dialogue ...')