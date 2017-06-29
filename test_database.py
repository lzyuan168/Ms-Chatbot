import unittest
from database import *


""" Test database file """
class TestDatabase(unittest.TestCase):

	""" SetUp initial condition -- which is an empty test database """
	def setUp(self):
		print("In setUp")

	""" TearDown to prepare for next test -- empty out the database """
	def tearDown(self):
		print("In tearDown")
		delete_all("test")
		reset_auto_increment("test")

	""" Description: Test add_data function to see if the data are correctly added to database in correct format """
	def test_add_data(self):
		test_add = add_data("user_123", "This is test", "test entity", "test value", "test")
		test_read = read_data("user_123", "test")
		expected_output = [[1, 'user_123', 'This is test', 'test entity', 'test value']]
		self.assertEqual(test_read, expected_output)

	""" Description: Test read_data function to see if the correct data is read """
	def test_read_data(self):
		data1 = add_data("user_111", "This is first", "entity 1", "value 1", "test")
		data2 = add_data("user_222", "This is second", "entity 2", "value 2", "test")
		test_read = read_data("user_111", "test")
		expected_output = [[1, "user_111", "This is first", "entity 1", "value 1"]]
		self.assertEqual(test_read, expected_output)

	""" Description: Test read_last_data function to see if the lastest added data by the same user is correctly read """
	def test_read_last_data(self):
		data1 = add_data("user_111", "This is first", "entity 1", "value 1", "test")
		data2 = add_data("user_111", "This is second", "entity 2", "value 2", "test")
		test_read = read_last_data("user_111", "test")
		expected_output = [[2, "user_111", "This is second", "entity 2", "value 2"]]
		self.assertEqual(test_read, expected_output)

	""" Description: Test update_read function to see if the correct data is returned by specifying entity and user_id """
	def test_update_read(self):
		data1 = add_data("user_111", "This is first", "entity 1", "value 1", "test")
		data2 = add_data("user_111", "This is second", "entity 2", "value 2", "test")
		data3 = add_data("user_222", "This is second", "entity 2", "value 2", "test")
		test_read = update_read("user_222", "entity 2", "test")
		expected_output = [[3, "user_222", "This is second", "entity 2", "value 2"]]
		self.assertEqual(test_read, expected_output)

	""" Description: Test update_data function to see if the reply and value will be updated by selecting data based on original reply and entity 
		Observation: update_data does not output any value thus if test_read is == expected_output after update_data then its good"""
	def test_update_data(self):
		data = add_data("user_111", "This is original", "entity original", "value original", "test")
		test_update = update_data("user_111", "This is updated", "value updated", "This is original", "entity original", "test")
		test_read = read_data("user_111", "test")
		expected_output = [[1, "user_111", "This is updated", "entity original", "value updated"]]
		self.assertEqual(test_read, expected_output)

	""" Description: Test delete_data function to see if the correct data will be deleted by selecting data based on reply and entity 
		Observation: test_read should output data2, if test_read == expected_output after deleting data1 then its good"""
	def test_delete_data(self):
		data1 = add_data("user_111", "This is reply 1", "entity 1", "value same", "test")
		data2 = add_data("user_111", "This is reply 2", "entity 2", "value same", "test")
		test_delete = delete_data("user_111", "This is reply 1", "entity 1", "test")
		test_read = read_data("user_111", "test")
		expected_output = [[2,"user_111", "This is reply 2", "entity 2", "value same"]]
		self.assertEqual(test_read, expected_output)




if __name__ == "__main__":
	unittest.main(verbosity=2)