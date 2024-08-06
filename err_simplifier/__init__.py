from .logger import log_message, handle_exception, simplify_message
import colorama as colorama
from colorama import  init, Fore, Style
import datetime as datetime
import pip
import flask
pip.main(['install','flask'])
pip.main(['install','pip'])
pip.main(['install','colorama'])
pip.main(['install','os'])