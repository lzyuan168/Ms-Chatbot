import os, sys
from flask import Flask, request
from utils import wit_response
from rest_api import Bot
from database import *
from parser_helper import *
from config import Config
import json


app = Flask(__name__)

PAGE_ACCESS_TOKEN = "EAADEvommVxABAF3mWLwlW00piWsVfxPpqOarmgpYV7focZC0jlfJXhEsqQOsY7NF97ko206litHprDMxmG8zaoJnjwZCPARHr8ImF1Dvuyh6EDIONZAkIKTzXbR3tyZBSkrvDGNfxq5MYJ8asBXeVcgZAZCvbHqmakyTQgryuwtAZDZD"

bot = Bot(PAGE_ACCESS_TOKEN)


@app.route('/setup', methods=['GET'])
def set_get_started_button():
    payload = {
      "get_started":{
        "payload":"Get Started"
      }
    }

    r = bot.send_start(payload)
    return "ok", 200


@app.route('/', methods=['GET'])
def verify():
    ### webhook verification
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == "hello":
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200
    return "Hello world", 200


@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()
    log(data)

    if data['object'] == 'page':
        for entry in data['entry']:
            for messaging_event in entry['messaging']:

                ### ID
                sender_ID = messaging_event['sender']['id']
                recipient_ID = messaging_event['recipient']['id']

                ### "message" type received from user
                if messaging_event.get('message'):

                    ### text message
                    if 'text' in messaging_event['message']:
                        messaging_text = messaging_event['message']['text']
                        messaging_text = messaging_text.lower()

                    ### other types of message
                    else:
                        messaging_text = 'no text'

                    info = user_info(sender_ID)
                    log(info)

                    ### responses to user intputs
                    bot_typing_on_off(sender_ID, "typing_on")
                    msg_list = wit_response(messaging_text)
                    text_message_handling(sender_ID, recipient_ID, msg_list)

                ### "postback" type received from user
                elif messaging_event.get('postback'):

                    ### button's payload
                    messaging_text = messaging_event['postback']['payload']
                    #messaging_text = messaging_text.lower()

                    log("Inside postback")
                    log(messaging_text)

                    info = user_info(sender_ID)
                    log(info)

                    ### handles the payload
                    bot_typing_on_off(sender_ID, "typing_on")
                    payload_handler(sender_ID, messaging_text)


    return "ok", 200



########################
### Handler Function ###
########################

entities = ['location', 'datetime', 'duration', \
            'adults', 'children', 'number']

question_dict = {'origin':'Where are you travelling from?',
                 'destination':'Which country are you going to?',
                 'datetime':'When are you going to travel?',
                 'duration':'How long are you going to travel for?',
                 'adults':'How many adults are there?',
                 'children':'How many children(below 18 years of age) are there?',
                 'number':'How many people are travelling? Please reply in terms of number of adults and children(below 18 years of age). Example, 1 adult 0 child.',
                 'who':'Who is/are travelling? Please reply in terms of number of adults and children(below 18 years of age). Example, 1 adult 0 child.'}


def text_message_handling(sender_id, recipient_id, msg_list):

    ### adding to database
    add_to_database(sender_id, msg_list)

    ### reading all data and adding to entity_list
    entity_list = reading_data(sender_id)

    ### returns a single last(latest) user input
    single_data = read_last_data(sender_id)

    ### check the intention of the user input and reply accordingly
    check_msg_intention(sender_id, recipient_id, single_data, entity_list, question_dict, entities)
    #bot_typing_on_off(sender_id, "typing_off")
    #bot_text_reply(sender_id, reply)


def payload_handler(sender_id, messaging_text):
    
    ### getting started and selecting type of travel insurance
    if messaging_text == "Get Started":
        reply = "Hello there. Welcome to MoneySmart.\nI am here to help you" + \
                " get the best deal for Travel Insurance."

        text = "Which type of Travel Insurance are you looking for?"
        buttons = [{"type":"postback",
                    "title":"Single Trip",
                    "payload":"Single Trip"},
                   {"type":"postback",
                    "title":"Annual Coverage",
                    "payload":"Annual Coverage"}]

        bot_text_reply(sender_id, reply)
        bot_button_msg(sender_id, text, buttons)

    ### if single trip is selected
    elif messaging_text == "Single Trip":
        text = "Thank you for selecting Single Trip Insurance\n\n" \
               "Before I bring the deals to you" \
               " I'll need some details from you.\n\nFor a start you may want" + \
               " to tell me if your departure city is Singapore?"
        buttons = [{"type":"postback",
                    "title":"Yes",
                    "payload":"Yes"},
                   {"type":"postback",
                    "title":"No",
                    "payload":"No"}]
        add_data(sender_id, "single trip insurance", "", "")
        bot_button_msg(sender_id, text, buttons)

    ### departure city checking
    elif messaging_text == "Yes":
        reply = str(question_dict.get('destination'))
        add_data(sender_id, "from singapore", "origin", "singapore")
        bot_text_reply(sender_id, reply)        

    elif messaging_text == "No":
        reply = "I'm sorry. In order to be eligible for the insurance, your departure" \
                " city has to be Singapore. Thank you for visiting MoneySmart"
        bot_text_reply(sender_id, reply)




#######################
### Helper Function ###
#######################

os.environ["DATABASE_NAME"] = "insurance"

def add_to_database(sender_id, msg_list):

    user_reply = msg_list[0][0]

    ### check if there are entities involved
    if len(msg_list) > 1:
        ### other than reply message, there is at least 1 entity, value pair
        for i in range(1, len(msg_list)):
            entity = msg_list[i][0]
            value = msg_list[i][1]
            add_data(sender_id, user_reply, entity, value)
    ### else just add reply message
    else:
        add_data(sender_id, user_reply, "", "")


def reading_data(sender_id):

    ### read all input from user
    data_list = read_data(sender_id)
    entity_list = []

    for lst in data_list:
        entity_list.append(lst[3])

    return entity_list


### check the intention of user input and reply accordingly
def check_msg_intention(sender_id, recipient_id, twoD_list, entity_list, question_dict, entities):

    reply_list = twoD_list[0]
    entity = reply_list[3]
    value = reply_list[4]
    data_list = read_data(sender_id)
    reply = ""
    confirm = confirmation_msg(data_list)

    def greeting_msg():
        reply = "Hello there. Welcome to MoneySmart.\nI am here to help you" + \
                " get the best deal for Travel Insurance."
        return reply

    def travel_prompt():
        text = "I'll need some details from you.\n\nFor a start you may want" + \
                " to tell me if your departure city is Singapore?"
        buttons = [{"type":"postback",
                    "title":"Yes",
                    "payload":"Yes"},
                   {"type":"postback",
                    "title":"No",
                    "payload":"No"}]

        return bot_button_msg(sender_id, text, buttons)

    def unknown_msg():
        reply = "I'm sorry, I don't understand what you said. You may want" + \
                " to ask me about Travel Insurance."
        return reply

    def update_msg():
        data = update_read(sender_id, entity)
        reply_original = data[0][2]
        reply_updated = reply_list[2]
        value_updated = reply_list[4]

        delete_data(sender_id, reply_updated, entity)
        update_data(sender_id, reply_updated, value_updated, reply_original, entity)

        if entity == "datetime":
            reply = "You have updated your {} to {}".format(entity, value_updated[0:10])
        elif entity == "adults" or entity == "children":
            if "adults" or "adult" and "children" or "child" in reply_updated:
                msg = msg_parser(reply_updated)
                A_number = ""
                C_number = ""
                for item in msg:
                    if item == "children" or item == "child":
                        C_number = msg[msg.index(item)-1]
                    if item == "adults" or item == "adult":
                        A_number = msg[msg.index(item)-1]
                reply = "You have updated the number of adults to {} and children to {}".format(A_number, C_number)
            elif "adults" or "adult" in reply_updated:
                msg = msg_parser(reply_updated)
                for item in msg:
                    if item == "adults" or item == "adult":
                        number = msg[msg.index(item)-1]
                reply = "You have updated the number of {} to {}".format(entity, number)
            elif "children" or "child" in reply_updated:
                msg = msg_parser(reply_updated)
                for item in msg:
                    if item == "children" or item == "child":
                        number = msg[msg.index(item)-1]
                reply = "You have updated the number of {} to {}".format(entity, number)
        else:
            reply = "You have updated your {} to {}".format(entity, value_updated)
        return reply

    def confirm_msg():
        #confirm = confirmation_msg(data_list)
        reply = "Let me confirm the information you have provided.\n\n{}".format(confirm) + \
                "\n" + \
                "Now I will bring you the best deal."
        return reply

    def next_question():
        for item in entities:
            if item not in entity_list:
                if item == "adults" or item == "children":
                    reply = str(question_dict.get('who'))
                else:
                    reply = str(question_dict.get(item))
                    break
        return reply


    ### if greeting message
    if "greetings" in reply_list:
        reply = greeting_msg()
        bot_text_reply(sender_id, reply)

    ### travel insurance prompt
    elif "travel insurance" in reply_list[2]:
        travel_prompt()

    ### if entity, value are missing. This is unknown message.
    elif entity == "" and value == "":
        reply = unknown_msg()
        bot_text_reply(sender_id, reply)

    ### flexible input
    elif entity == "location":
        bot_reply = read_last_data(recipient_id)
        if bot_reply[0][2] == question_dict.get('destination').lower():
            add_data(sender_id, "going to {}".format(value), "destination", value)
            reply = next_question()
        bot_text_reply(sender_id, reply)

    ### change and update any existing criteria
    elif entity in entity_list and entity_list.count(entity) > 1:
        question = ""
        if set(entities) <= set(entity_list):
            reply = confirm_msg()
        else:
            reply = update_msg()
            question = next_question()
        bot_text_reply(sender_id, reply)
        bot_text_reply(sender_id, question)

    ### all criteria are met
    elif set(entities) <= set(entity_list):
        reply = confirm_msg()
        bot_text_reply(sender_id, reply)

    ### asking the next question
    else:
        reply = next_question()
        bot_text_reply(sender_id, reply)



### the confirmation message that is returned when all critrias are met
def confirmation_msg(data_list):
    confirmaton_msg = ""
    origin_msg = "You are travelling from Singapore"
    dest_msg = ""
    duration_msg = ""
    date_msg = ""
    adult_msg = ""
    children_msg = ""

    for data in data_list:
        #if data[3] == "origin":
            #origin_msg = "You are travelling from {}".format(data[4])

        if data[3] == "destination":
            dest_msg = " to {}".format(data[4])

        elif data[3] == "duration":
            parsed = msg_parser(data[2])
            quantity = ""
            for item in parsed:
                if item == data[4] or item == "a":
                    index = parsed.index(item)
                    quantity = parsed[(index+1)]

            duration_msg = " for {} {}.".format(data[4], quantity)

        elif data[3] == "datetime":
            date = data[4][0:10]
            date_msg = " You are going on {}".format(date)

        elif data[3] == "adults":
            parsed = msg_parser(data[2])
            number = ""
            for item in parsed:
                if item == "adults" or item == "adult":
                    index = parsed.index(item)
                    number = parsed[(index-1)]
                    pass

            if number == '1':
                adult_msg = " with a total of 1 adult"
            else:
                adult_msg = " with a total of {} {}".format(number, data[4])

        elif data[3] == "children":
            parsed = msg_parser(data[2])
            number = ""
            for item in parsed:
                if item == "children" or item == "child":
                    index = parsed.index(item)
                    number = parsed[(index-1)]
                    pass

            if number == '0':
                children_msg = " and no children."
            elif number == '1':
                children_msg = " and 1 child."
            else:
                children_msg = " and {} {}.".format(number, data[4])

    return(origin_msg + dest_msg + duration_msg + date_msg + adult_msg + children_msg)



#############################
### Bot Related Functions ###
#############################

def bot_text_reply(sender_id, response):
    bot.send_text_message(sender_id, response)
    return "ok", 200


def bot_typing_on_off(sender_id, action):
    ### action: action type(mark_seen, typing_on, typing_off)
    bot.send_action(sender_id, action)
    return "ok", 200


def bot_button_msg(sender_id, text, buttons):
    ### buttons are in json format
    bot.send_button_message(sender_id, text, buttons)
    return "ok", 200


@app.route('/', methods=['GET'])
def user_info(user_id):
    fields = ["first_name", "last_name", "locale", "timezone", "is_payment_enabled"]
    r = bot.get_user_info(user_id, fields)
    return "ok", 200



############
### Misc ###
############

def log(message):
    print(message)
    sys.stdout.flush() ### ensure complete printing of msg output


if __name__ == "__main__":
    app.run(debug = True, port = 80)
