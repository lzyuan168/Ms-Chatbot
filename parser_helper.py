import re
import json

def msg_parser(message_text):
    return re.split('\W+', message_text)