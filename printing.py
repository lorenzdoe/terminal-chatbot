import re
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import TerminalFormatter

def color_string(word: str, color: str) -> str:
    colors = {
        'red': '\033[91m',
        'green': '\033[92m',
        'yellow': '\033[93m',
        'blue': '\033[94m',
        'magenta': '\033[95m',
        'cyan': '\033[96m',
    }
    end_color = '\033[0m'
    
    if color not in colors:
        return word  # without color if color is not found
    else:
        colored_word = colors[color] + word + end_color
        return colored_word

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
            opening, end = color_string('CODE\n>>>', 'red'), color_string('\n<<<\nCODE END','red')
            formatted_code = opening + '\n'.join(formatted_code.splitlines()) + end  # Remove the extra line breaks
            text = text.replace('```{}```'.format(match), formatted_code)
        except Exception as e:
            print(type(e))
            print('Error when formatting code: {}'.format(e))

    return text

def print_instructions() -> None:
    print('''
Ctrl+C or exit  ... exit program
save            ... save conversation
usage           ... print usage
read            ... read file''')
    
def print_response_formatted(response: str) -> None:
    response_formatted = format_code(response)
    opener, end = color_string('---------------  GPT  ---------------', 'magenta'), color_string('---------------  ---  ---------------', 'magenta')
    print('\n{}\n{}\n{}'.format(opener, response_formatted, end))

def print_usage() -> None:
    print('''
 -h, --help             print the help for the program
 -p, --prompt           pass a prompt for processing
 -r, --read <file>      pass a file to be read
''')