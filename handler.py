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

    def __init__(self, chatbot: Chatbot) -> None:
        self.chatbot = chatbot
        self.current_prompt = ''
        self.__passed_prompt = False
        self.prompt_actions = {
            'exit': lambda: sys.exit(0),
            'usage': self.handle_usage,
            'save': self.handle_save,
            'read': self.handle_read,
            '': lambda: print('\nempty prompt ...')
        }

    def handle_usage(self) -> None:
        # clear prompt and print instructions
        self.current_prompt = ''
        print_instructions()

    def handle_save(self) -> None:
        # clear prompt
        self.current_prompt = ''

        file_path: str = asksaveasfilename(defaultextension='.txt', filetypes=[('Text Files', '*.txt'), ('All Files', '*.*')])

        try:
            with open(file_path, 'w') as file:
                # Iterate over list and write each item
                for message in self.chatbot.conversation:
                    file.write('{}:\n{}\n--------------------\n'.format(message['role'],message['content']))
            print('\nwriting conversation to: {}'.format(file_path))
            file.close()
        except Exception as e:
            print('\nAn error occurred while writing the file: {}'.format(str(e)))
    
    def handle_read(self, file_path: str = None) -> None:
        # clear prompt
        if not self.__passed_prompt:
            self.current_prompt = ''

        if file_path == None:
            file_path = askopenfilename(defaultextension='.txt', filetypes=[('Text Files', '*.txt'), ('All Files', '*.*')])

        try:
            with open(file_path, 'r') as file:
                self.current_prompt += file.read()
            print('\nreading following file: {}'.format(file_path))
        except FileNotFoundError:
            print('\nFile not found.')
        except Exception as e:
            print('\nAn error occurred while reading the file: {}'.format(str(e)))


    def handle_prompt(self) -> None:
        action = self.prompt_actions.get(self.current_prompt)
        if action:
            action()
        else:
            response: str = self.chatbot.get_response(self.current_prompt)
            print_response_formatted(response)
            self.current_prompt = ''
    
    def parse_options(self, argv: list) -> None:
        short_options: str = 'hr:p:'
        long_options: list = ['help', 'read=', 'prompt=']

        # parse the command-line arguments
        arguments, values = getopt.getopt(argv[1:], short_options, long_options)

        # process arguments
        for current_argument, current_value in arguments:
            if current_argument in ('-r', '--read'):
                self.handle_read(current_value)

            elif current_argument in ('-p', '--prompt'):
                self.current_prompt += current_value
                print('\nhandling following prompt: {}'.format(current_value))
                self.__passed_prompt = True
            
            elif current_argument in ('-h', '--help'):
                print('Usage: {} [options...]'.format(argv[0]))
                print_usage()
                sys.exit(0)

        
        # treat remaining arguments as prompt and append it to the prompt
        self.current_prompt += ' '.join(values)

    def convo(self, argv: list) -> None:
        self.parse_options(argv)
        print_instructions()

        
        if self.__passed_prompt:
            self.__passed_prompt = False
            self.handle_prompt()
    
        while True:
            try:
                self.current_prompt += input('\nprompt: ')
                self.handle_prompt()
            except SystemExit:
                break
            except:
                print('continue dialogue ...\n')