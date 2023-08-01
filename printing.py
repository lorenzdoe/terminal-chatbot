
def print_instructions() -> None:
    print('''
Ctrl+C or exit  ... exit program
save            ... save conversation
usage           ... print usage
read            ... read file
          ''')
    
def print_response_formatted(message: str) -> None:
    print('\n---------------  GPT  ---------------\n{}\n---------------  ---  ---------------'.format(message))

def print_usage() -> None:
    print('''
 -h, --help             print the help for the program
 -p, --prompt           pass a prompt for processing
 -r, --read <file>      pass a file to be read
''')