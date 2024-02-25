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
from _tkinter import TclError

HEADLESS: bool = False

# define signal handler functions
def signal_handler_exit(sig, frame) -> None:
    print('\nCtrl+C pressed. Exiting gracefully.')
    sys.exit(0)

# register signal handler
signal.signal(signal.SIGINT, signal_handler_exit)

if __name__ == '__main__':
    try:
        root = Tk()        # create Tkinter root window
        root.withdraw()    # Hide root window
    except TclError:
        HEADLESS = True
        print("INFO: No display found. Running in headless mode.")

    # starts the conversation
    handler: Handler = Handler(headless=HEADLESS)
    handler.initiate_conversation(sys.argv)