#!/bin/python3
'''
terminal-gpt
gpt chatbot for the terminal
OpenAI key needs to be exported to OPENAI_API_KEY environment variable
'''
import sys
import signal
from tkinter import Tk
from handler import Handler

# define signal handler functions
def signal_handler_exit(sig, frame) -> None:
    print('\nCtrl+C pressed. Exiting gracefully.')
    sys.exit(0)

# register signal handler
signal.signal(signal.SIGINT, signal_handler_exit)

if __name__ == '__main__':
    # create Tkinter root window
    root = Tk()
    # Hide root window
    root.withdraw()

    # starts the conversation
    handler: Handler = Handler()
    handler.convo(sys.argv)