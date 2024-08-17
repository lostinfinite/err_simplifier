from .logger import log_message, handle_exception, simplify_message
import colorama as colorama
from colorama import  init, Fore, Style
import datetime as datetime
import pip
import flask
import time

pip.main(['install','time'])
pip.main(['install','flask'])
pip.main(['install','pip'])
pip.main(['install','colorama'])
pip.main(['install','os'])