import unittest
from app import *


""" Test the utils file """
class TestUtils(unittest.TestCase):

	""" Description: Test wit_response to see if it correctly interpret the user input and output the correct entity, value pairs.
	    Expected outcome: It should output a list of lists where the first element is the user input and the rest of the elements are the entity, value pairs"""
	def test_wit_response(self):
		user_input = "i am going from singapore to france next week for 3 days with 2 adults and 2 children"
		wit_res = wit_response(user_input)
		expected_output = [['i am going from singapore to france next week for 3 days with 2 adults and 2 children'], ['who', 'i'], ['origin', 'singapore'], ['destination', 'france'], ['datetime', '2017-07-03T00:00:00.000+08:00'], ['duration', 3], ['number', 2], ['adults', 'adults'], ['children', 'children']]
		self.assertEqual(wit_res, expected_output)


""" Test parser_helper file """
class TestParserHelper(unittest.TestCase):

	""" Description: Test parser_helper to see if it will parse the user input into each individual words """
	def test_msg_parser(self):
		message_text = "i am going to france test-test you/me\our"
		parse_res = msg_parser(message_text)
		expected_output = ['i', 'am', 'going', 'to', 'france', 'test', 'test', 'you', 'me', 'our']
		self.assertEqual(parse_res, expected_output)


""" Test database file """
class TestDatabase(unittest.TestCase):

	""" Description: Test add_data function to see if the data are correctly added to database in correct format """
	def test_add_data(self):
		pass 


if __name__ == "__main__":
	unittest.main(verbosity=2)