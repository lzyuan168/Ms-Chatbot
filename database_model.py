from peewee import *
import MySQLdb
from config import Config

db = MySQLDatabase(Config.get_database(), host=Config.get_host(), user=Config.get_user(), password=Config.get_password())

def open_connection():
    db.connect()

def close_connection():
    db.close()

def print_read_data(query):
    lst = []
    for elem in query:
        lst.append([elem.user_id, elem.reply, elem.entity, elem.value])
    return lst


class BaseModel(Model):
    class Meta:
        database = db


class UserReply(BaseModel):
    user_id = TextField()
    reply = TextField()
    entity = TextField()
    value = TextField()

    class Meta:
        db_table = 'User_reply'


    # function for adding data
    def add_data(user_id, reply, entity, value):

        open_connection()

        query = UserReply.insert(user_id=user_id, reply=reply, entity=entity, value=value)
        query.execute()

        close_connection()

    # function for reading data
    def read_data(user_id):

        open_connection()

        query = UserReply.select().where(UserReply.user_id == user_id)
        result_list = print_read_data(query)

        close_connection()

        return result_list


    # function for getting the user last response
    def read_last_data(user_id):

        open_connection()
        
        query = UserReply.select().where(UserReply.user_id == user_id).order_by(UserReply.id.desc()).limit(1)
        result_list = print_read_data(query)

        close_connection()

        return result_list


    # reading data for update
    def update_read(user_id, entity):

        open_connection()

        query = UserReply.select().where((UserReply.user_id == user_id) & (UserReply.entity == entity))
        result_list = print_read_data(query)

        close_connection()

        return result_list


    # updating the data in the table
    def update_data(user_id, reply_updated, value_updated, reply_original, entity):

        open_connection()

        query = UserReply.update(reply=reply_updated, value=value_updated).where((UserReply.user_id == user_id) & (UserReply.reply == reply_original) & (UserReply.entity == entity))
        query.execute()

        close_connection()


    # delete the selected data in the table
    def delete_data(user_id, reply, entity):

        open_connection()

        query = UserReply.delete().where((UserReply.user_id == user_id) & (UserReply.reply == reply) & (UserReply.entity == entity))
        query.execute()

        close_connection()


    # delete everything from the table
    def delete_all():

        open_connection()

        query = UserReply.delete()
        query.execute()

        close_connection()


    # reset auto increment to 1
    def reset_auto_increment():
        # open database connection
        connection = MySQLdb.connect(Config.get_host(), Config.get_user(), Config.get_password(), Config.get_database())

        # prepare a cursor object using cursor() method
        cursor = connection.cursor()

        sql = "ALTER TABLE User_reply AUTO_INCREMENT = 1"

        cursor.execute(sql)
        connection.commit()
        cursor.close()
        connection.close()