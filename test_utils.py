import unittest
from utils import wit_response


# Test the utils file
class TestUtils(unittest.TestCase):

	""" Description: Test wit_response to see if it correctly interpret the user input and output the correct entity, value pairs.
	    Expected outcome: It should output a list of lists where the first element is the user input and the rest of the elements are the entity, value pairs"""
	def test_wit_response(self):
		user_input = "i am going from singapore to france next week for 3 days with 2 adults and 2 children"
		wit_res = wit_response(user_input)
		expected_output = [['i am going from singapore to france next week for 3 days with 2 adults and 2 children'], ['who', 'i'], ['origin', 'singapore'], ['destination', 'france'], ['datetime', '2017-07-03T00:00:00.000+08:00'], ['duration', 3], ['number', 2], ['adults', 'adults'], ['children', 'children']]
		self.assertEqual(wit_res, expected_output)


if __name__ == "__main__":
	unittest.main(verbosity=2)