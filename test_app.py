import unittest
from unittest.mock import Mock
from database_model import *
from app import *

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


# test for app.py file
class TestApp(unittest.TestCase):

    # SetUp initial condition -- which is an empty test database
    def setUp(self):
        print("In setUp")

    # TearDown to prepare for next test -- empty out the database
    def tearDown(self):
        print("In tearDown")
        UserReply.delete_all()
        UserReply.reset_auto_increment()
    
    # To test if text messages are being handled correctly when the user typed a message
    def test_text_message_handling(self):
        msg_list = [["This is a test user reply"], ["sample entity 1", "sample value 1"], ["sample entity 2", "sample value 2"]]
        sender_id = "test_user_1"
        add_to_database(sender_id, msg_list)

        test_entity_list = reading_data(sender_id)
        expected_entity_list = ["sample entity 1", "sample entity 2"]
        self.assertEqual(test_entity_list, expected_entity_list)

        test_single_data = UserReply.read_last_data(sender_id)
        expected_single_data = [["test_user_1", "This is a test user reply", "sample entity 2", "sample value 2"]]
        self.assertEqual(test_single_data, expected_single_data)
        
        mock_check_msg_intention(sender_id, recipient_id, test_single_data, test_entity_list, question_dict, entities)
        # assert that mock_check_msg_intention is called with the given arguments
        self.assertTrue((mock_check_msg_intention.call_args == ((sender_id, recipient_id, test_single_data, test_entity_list, question_dict, entities),)))


    # To test if payload messages are being handled correctly when user clicked on a button
    def test_payload_handler(self):
        # make assertion that the method is being called when the correct parameters are passed to it
        pass


    """ Description: To test if user's messages are successfully being add to database
        Observation: There are 2 kinds of msg_list, one which contains entity, value pair and one which doesn't
                     The result should be different
    """
    def test_add_to_database(self):

        # user input with entity and value
        msg_list_long = [["This is a long test user reply"], ["sample entity 1", "sample value 1"], ["sample entity 2", "sample value 2"]]
        sender_id_1 = "test_user_1"
        test_function_long = add_to_database(sender_id_1, msg_list_long)
        test_result_long = UserReply.read_data(sender_id_1)
        expected_result_long = [["test_user_1", "This is a long test user reply", "sample entity 1", "sample value 1"], ["test_user_1", "This is a long test user reply", "sample entity 2", "sample value 2"]]
        self.assertEqual(test_result_long, expected_result_long)
        
        # user input without entity and value
        msg_list_short = [["This is a short test user reply"]]        
        sender_id_2 = "test_user_2"        
        test_function_short = add_to_database(sender_id_2, msg_list_short)        
        test_result_short = UserReply.read_data(sender_id_2)        
        expected_result_short = [["test_user_2", "This is a short test user reply", "", ""]]        
        self.assertEqual(test_result_short, expected_result_short)


    # To test if correct data are being read from the database using user's sender_id
    def test_reading_data(self):
        sender_id = "test_user_1"
        reply = "This is test reply"
        entity_1 = "sample entity 1"
        entity_2 = "sample entity 2"
        value_1 = "sample value 1"
        value_2 = "sample value 2"
        UserReply.add_data(sender_id, reply, entity_1, value_1)
        UserReply.add_data(sender_id, reply, entity_2, value_2)
        test_result = reading_data(sender_id)
        expected_result = ["sample entity 1", "sample entity 2"]
        self.assertEqual(test_result, expected_result)


    """ Description: To test if the correct message intention is being selected when specific keyword
                     is present.
        Observation: Example when "greeting" is present, return greeting_msg() etc
    """
    def test_check_msg_intention(self):
        sender_id = "test_user_1"
        recipient_id = "test_recipient_1"
        test_greet_list = [["test_user_1", "Test greet", "greetings", "hello"]]
        pass


    # To test if the correct confirmation message is return to users when all the necessary information is collected
    def test_confirmation_msg(self):
        data_list = [["test_user_1", "from singapore", "origin", "singapore"],
                     ["test_user_1", "thailand", "destination", "thailand"],
                     ["test_user_1", "next week", "datetime", "2017-07-17T00:00:00.000+08:00"],
                     ["test_user_1", "5 days", "duration", "5"],
                     ["test_user_1", "2 adults 2 children", "adults", "adults"],
                     ["test_user_1", "2 adults 2 children", "children", "children"]]
        test_result = confirmation_msg(data_list)
        expected_result = "You are travelling from Singapore to thailand for 5 days. You are going on 2017-07-17 with a total of 2 adults and 2 children."
        self.assertEqual(test_result, expected_result)


if __name__ == "__main__":
    unittest.main(verbosity=2)