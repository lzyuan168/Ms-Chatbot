import re
import json

def msg_parser(message_text):
    return re.split('\W+', message_text)


#print(msg_parser("25/6/2017"))
#reply = msg_parser("i am going to france test-test you/me\our")
#print(reply[reply.index("going")-1])



