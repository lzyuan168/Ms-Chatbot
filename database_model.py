from peewee import *
import MySQLdb
from config import Config

db = MySQLDatabase(Config.get_database(), host=Config.get_host(), user=Config.get_user(), password=Config.get_password())

class BaseModel(Model):
    class Meta:
        database = db


class User_reply(BaseModel):
    user_id = TextField()
    reply = TextField()
    entity = TextField()
    value = TextField()


def open_connection():
    db.connect()

def close_connection():
    db.close()

def print_read_data(query):
    lst = []
    for elem in query:
        lst.append([elem.user_id, elem.reply, elem.entity, elem.value])
    return lst


# function for adding data
def add_data(user_id, reply, entity, value):

    open_connection()

    query = User_reply.insert(user_id=user_id, reply=reply, entity=entity, value=value)
    query.execute()

    close_connection()

# function for reading data
def read_data(user_id):

    open_connection()

    query = User_reply.select().where(User_reply.user_id == user_id)
    result_list = print_read_data(query)

    close_connection()

    return result_list


# function for getting the user last response
def read_last_data(user_id):

    open_connection()
    
    query = User_reply.select().where(User_reply.user_id == user_id).order_by(User_reply.id.desc()).limit(1)
    result_list = print_read_data(query)

    close_connection()

    return result_list


# reading data for update
def update_read(user_id, entity):

    open_connection()

    query = User_reply.select().where((User_reply.user_id == user_id) & (User_reply.entity == entity))
    result_list = print_read_data(query)

    close_connection()

    return result_list


# updating the data in the table
def update_data(user_id, reply_updated, value_updated, reply_original, entity):

    open_connection()

    query = User_reply.update(reply=reply_updated, value=value_updated).where((User_reply.user_id == user_id) & (User_reply.reply == reply_original) & (User_reply.entity == entity))
    query.execute()

    close_connection()


# delete the selected data in the table
def delete_data(user_id, reply, entity):

    open_connection()

    query = User_reply.delete().where((User_reply.user_id == user_id) & (User_reply.reply == reply) & (User_reply.entity == entity))
    query.execute()

    close_connection()


# delete everything from the table
def delete_all():

    open_connection()

    query = User_reply.delete()
    query.execute()

    close_connection()


# reset auto increment to 1
def reset_auto_increment():
    # open database connection
    connection = MySQLdb.connect(Config.get_host(), Config.get_user(), Config.get_password(), Config.get_database())

    # prepare a cursor object using cursor() method
    cursor = connection.cursor()

    sql = "ALTER TABLE user_reply AUTO_INCREMENT = 1"

    cursor.execute(sql)
    connection.commit()
    cursor.close()
    connection.close()