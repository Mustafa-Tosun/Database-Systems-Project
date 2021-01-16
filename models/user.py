from flask import current_app
from flask_login import UserMixin
import pymysql
connection = pymysql.connect("sql7.freemysqlhosting.net","sql7387357","KdlqtCZW85","sql7387357" )

class User(UserMixin):
    def __init__(self, email, password, username="", realname="", is_admin=0, id=""):
        self.id = id
        self.email = email
        self.password = password
        self.username = username
        self.realname = realname
        self.is_admin = is_admin
        self.active = True

    def get_id(self):
        return self.id
    
    @property
    def is_active(self):
        return self.active


def add_user(user):
    cursor = connection.cursor()
    query = "INSERT INTO user(username, email, password, realname) VALUES(%s, %s, %s, %s)"
    cursor.execute(query, (user.username, user.email, user.password, user.realname))
    connection.commit()
    cursor.close()

def get_user_by_email(email):
    cursor = connection.cursor()
    query = "SELECT id, username, realname, is_admin, password FROM user WHERE email=%s"
    cursor.execute(query, email)
    connection.commit()
    try:
        id, username, realname, is_admin, password = cursor.fetchone()
        user = User(id=id, email=email, username=username, realname=realname, is_admin=is_admin, password=password)
    except:
        user = None
    cursor.close()
    return user

def get_user_by_id(id):
    cursor = connection.cursor()
    query = "SELECT username, email, realname, is_admin, password FROM user WHERE id=%s"
    cursor.execute(query, id)
    connection.commit()
    try:
        username, email, realname, is_admin, password = cursor.fetchone()
        user = User(id=id, email=email, username=username, realname=realname, is_admin=is_admin, password=password)
    except:
        user = None
    cursor.close()
    return user

def update_user(id, realname):
    cursor = connection.cursor()
    query = "UPDATE user SET realname=%s WHERE id=%s"
    cursor.execute(query, (realname, id))
    connection.commit()
    cursor.close()

def delete_user(id):
    cursor = connection.cursor()
    query = "DELETE FROM user WHERE id=%s"
    cursor.execute(query, id)
    connection.commit()
    cursor.close()