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

    def __init__(self, headless: bool = False) -> None:
        self.chatbot:           Chatbot = Chatbot()
        self.default_model:     str     = 'gpt-3.5-turbo-0125'
        self.current_prompt:    str     = ''
        self.headless_mode:     bool    = headless
        self.short_memory:      str     = ''        # memory for reading from file
        self.__passed_prompt:   bool    = False     # flag for passed prompt (as argument) -> handle it instantly
        self.chatbot.set_model(self.default_model)
        self.__setup_prompt_actions()
    
    def __setup_prompt_actions(self) -> None:
        self.prompt_actions = {
            'exit': lambda: sys.exit(0),
            'usage': self.__display_usage,
            'save': self.__save_conversation,
            'read': self.__read_from_file,
            '': lambda: None
        }

    def __display_usage(self) -> None:
        """Prints the usage instructions."""
        self.current_prompt = ''
        print_instructions()

    def __save_conversation(self) -> None:
        """Saves the conversation to a file."""
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
    
    def __read_from_file(self, file_path: str = None) -> None:
        """Reads the content of a file and appends it to the read memory."""

        self.current_prompt = ''

        if file_path == None:
            file_path = askopenfilename(defaultextension='.txt', filetypes=[('Text Files', '*.txt'), ('All Files', '*.*')]) if not self.headless_mode else input('Enter relative path: ')

        try:
            with open(file_path, 'r') as file:
                self.short_memory += file.read()
            print(f'\nreading following file: {file_path}')
        except FileNotFoundError:
            print('\nFile not found.')
        except Exception as e:
            print(f'\nAn error occurred while reading the file: {str(e)}')


    def __handle_prompt_input(self) -> None:
        action = self.prompt_actions.get(self.current_prompt)
        # handle case where there was read input but empty prompt -> call api
        action = None if self.short_memory and not self.current_prompt else action
        if action:
            action()
        else:
            full_prompt: str = self.short_memory + self.current_prompt
            response: str = self.chatbot.get_response(full_prompt)
            print_response_formatted(response)
            self.current_prompt = ''    # reset prompt
            self.short_memory    = ''    # reset read memory
    
    def parse_options(self, argv: list) -> None:
        short_options: str = 'hr:p:m:c:s:t:'
        long_options: list = ['help', 'read=', 'prompt=', 'model=', 'code=', 'shell=', 'translate=']

        # parse the command-line arguments
        try:
            arguments, values = getopt.getopt(argv[1:], short_options, long_options)
        except getopt.GetoptError as err:
            print(err)
            print_usage()
            sys.exit(2)

        # process arguments
        for current_argument, current_value in arguments:
            if current_argument in ('-r', '--read'):
                self.__read_from_file(current_value)
            elif current_argument in ('-p', '--prompt'):
                self.short_memory += f'{current_value}'
                self.__passed_prompt = True
                print(f'\nhandling following prompt: {current_value}')
            elif current_argument in ('-m', '--model'):
                model = 'gpt-4-turbo-preview' if current_value == '4' else self.default_model
                self.chatbot.set_model(model)
            elif current_argument in ('-h', '--help'):
                print(f'Usage: {argv[0]} [options...]')
                print_usage()
                sys.exit(0)
            elif current_argument in ('-c', '--code'):
                self.chatbot.set_system("""
You are a helpful assistant designed to output nothing more than the corresponding code for the message. 
Answer in python if the message does not specify the language.""")
                self.short_memory += f'{current_value}\n'
                self.__passed_prompt = True
            elif current_argument in ('-s', '--shell'):
                self.chatbot.set_system("""
You are a helpful assistant designed to output nothing more than the corresponding shell command for the message.
Answer in bash if the message does not specify the language.""")
                self.short_memory += f'{current_value}\n'
                self.__passed_prompt = True
            elif current_argument in ('-t', '--translate'):
                self.chatbot.set_system("""
You are a helpful assistant designed to output nothing more than the corresponding translation for the message.
Answer in english if the message does not specify the language.""")
                self.short_memory += f'{current_value}\n'
                self.__passed_prompt = True
        
        # treat remaining arguments as prompt and append it to the prompt
        self.current_prompt += ' '.join(values)

    def initiate_conversation(self, argv: list) -> None:
        self.parse_options(argv)
        print_instructions()
        print(f"\nmodel: {self.chatbot.get_model()}")
        
        # if prompt was passed as argument, handle it instantly without waiting for user input
        if self.__passed_prompt:
            self.__passed_prompt = False
            self.__handle_prompt_input()
    
        # main converstion loop
        while True:
            try:
                self.current_prompt = input('\nPrompt: ')
                self.__handle_prompt_input()
            except SystemExit:
                break
            except Exception as e:
                print(f'\nError: {e}')
                print('\ncontinue dialogue ...')