import unittest
from database import *


""" Test database file """
class TestDatabase(unittest.TestCase):

	""" Description: Test add_data function to see if the data are correctly added to database in correct format """
	def test_add_data(self):
		actual_add = add_data("user_123", "This is test", "entity", "value", "test")



if __name__ == "__main__":
	unittest.main(verbosity=2)