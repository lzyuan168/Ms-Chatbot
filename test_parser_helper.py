import unittest
from parser_helper import msg_parser


# Test parser_helper file
class TestParserHelper(unittest.TestCase):

	# Description: Test parser_helper to see if it will parse the user input into each individual words
	def test_msg_parser(self):
		message_text = "i am going to france test-test you/me\our"
		parse_res = msg_parser(message_text)
		expected_output = ['i', 'am', 'going', 'to', 'france', 'test', 'test', 'you', 'me', 'our']
		self.assertEqual(parse_res, expected_output)


if __name__ == "__main__":
	unittest.main(verbosity=2)