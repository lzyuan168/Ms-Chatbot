import unittest
from database_model import *
from config import Config


# Test database file
class TestDatabase(unittest.TestCase):

	# SetUp initial condition -- which is an empty test database
	def setUp(self):
		print("In setUp")

	# TearDown to prepare for next test -- empty out the database
	def tearDown(self):
		print("In tearDown")
		UserReply.delete_all()
		UserReply.reset_auto_increment()

	# Description: Test add_data function to see if the data are correctly added to database in correct format
	def test_add_data(self):
		test_add = UserReply.add_data("user_123", "This is test", "test entity", "test value")
		test_read = UserReply.read_data("user_123")
		expected_output = [['user_123', 'This is test', 'test entity', 'test value']]
		self.assertEqual(test_read, expected_output)

	# Description: Test read_data function to see if the correct data is read
	def test_read_data(self):
		data1 = UserReply.add_data("user_111", "This is first", "entity 1", "value 1")
		data2 = UserReply.add_data("user_222", "This is second", "entity 2", "value 2")
		test_read = UserReply.read_data("user_111")
		expected_output = [["user_111", "This is first", "entity 1", "value 1"]]
		self.assertEqual(test_read, expected_output)

	# Description: Test read_last_data function to see if the lastest added data by the same user is correctly read
	def test_read_last_data(self):
		data1 = UserReply.add_data("user_111", "This is first", "entity 1", "value 1")
		data2 = UserReply.add_data("user_111", "This is second", "entity 2", "value 2")
		test_read = UserReply.read_last_data("user_111")
		expected_output = [["user_111", "This is second", "entity 2", "value 2"]]
		self.assertEqual(test_read, expected_output)

	# Description: Test update_read function to see if the correct data is returned by specifying entity and user_id
	def test_update_read(self):
		data1 = UserReply.add_data("user_111", "This is first", "entity 1", "value 1")
		data2 = UserReply.add_data("user_111", "This is second", "entity 2", "value 2")
		data3 = UserReply.add_data("user_222", "This is second", "entity 2", "value 2")
		test_read = UserReply.update_read("user_222", "entity 2")
		expected_output = [["user_222", "This is second", "entity 2", "value 2"]]
		self.assertEqual(test_read, expected_output)

	""" Description: Test update_data function to see if the reply and value will be updated by selecting data based on original reply and entity 
		Observation: update_data does not output any value thus if test_read is == expected_output after update_data then its good"""
	def test_update_data(self):
		data = UserReply.add_data("user_111", "This is original", "entity original", "value original")
		test_update = UserReply.update_data("user_111", "This is updated", "value updated", "This is original", "entity original")
		test_read = UserReply.read_data("user_111")
		expected_output = [["user_111", "This is updated", "entity original", "value updated"]]
		self.assertEqual(test_read, expected_output)

	""" Description: Test delete_data function to see if the correct data will be deleted by selecting data based on reply and entity 
		Observation: test_read should output data2, if test_read == expected_output after deleting data1 then its good"""
	def test_delete_data(self):
		data1 = UserReply.add_data("user_111", "This is reply 1", "entity 1", "value same")
		data2 = UserReply.add_data("user_111", "This is reply 2", "entity 2", "value same")
		test_delete = UserReply.delete_data("user_111", "This is reply 1", "entity 1")
		test_read = UserReply.read_data("user_111")
		expected_output = [["user_111", "This is reply 2", "entity 2", "value same"]]
		self.assertEqual(test_read, expected_output)


if __name__ == "__main__":
	unittest.main(verbosity=2)