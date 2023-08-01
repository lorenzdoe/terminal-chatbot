#!/bin/python3
'''
terminal-gpt
gpt chatbot for the terminal
OpenAI key needs to be exported to OPENAI_API_KEY environment variable
'''
import sys
import signal
from tkinter import Tk
from api import Chatbot
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
    chatbot: Chatbot = Chatbot()
    chatbot.set_model('gpt-3.5-turbo')
    # chatbot.set_model('gpt-4')
    handler: Handler = Handler(chatbot)

    # starts the conversation
    handler.convo(sys.argv)