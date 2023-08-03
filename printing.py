import re
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import TerminalFormatter

def format_code(text):
    # Find all code snippets in the text
    matches = re.findall(r'```(.*?)```', text, re.DOTALL)
    
    # Replace each code snippet with its formatted version
    for match in matches:
        try:
            language = match.strip().splitlines()[0]
            code = '\n'.join(match.strip().splitlines())  # Extract the code portion
            lexer = get_lexer_by_name(language)
            formatted_code = highlight(code, lexer, TerminalFormatter())
            formatted_code = '```' + '\n'.join(formatted_code.splitlines()) + '\n```'  # Remove the extra line breaks
            text = text.replace('```{}```'.format(match), formatted_code)
        except Exception as e:
            print(type(e))
            print(e)

    return text

def print_instructions() -> None:
    print('''
Ctrl+C or exit  ... exit program
save            ... save conversation
usage           ... print usage
read            ... read file''')
    
def print_response_formatted(response: str) -> None:
    response_formatted = format_code(response)
    print('\n---------------  GPT  ---------------\n{}\n---------------  ---  ---------------'.format(response_formatted))

def print_usage() -> None:
    print('''
 -h, --help             print the help for the program
 -p, --prompt           pass a prompt for processing
 -r, --read <file>      pass a file to be read
''')