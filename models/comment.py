import pymysql
from server import connection
class Comment:
    def __init__(self, text, date, user_id, poem_id="", author_id="", id=""):
        self.id = id
        self.text = text
        self.date = date
        self.user_id = user_id
        self.poem_id = poem_id
        self.author_id = author_id

def add_comment(comment):
    cursor = connection.cursor()
    query = "INSERT INTO comment(text, date, user_id, poem_id, author_id) VALUES(%s, %s, %s, %s, NULL)"
    cursor.execute(query, (comment.text, comment.date, comment.user_id, comment.poem_id))
    connection.commit()
    cursor.close()

def add_comment_author(comment):
    cursor = connection.cursor()
    query = "INSERT INTO comment(text, date, user_id, author_id, poem_id) VALUES(%s, %s, %s, %s, NULL)"
    cursor.execute(query, (comment.text, comment.date, comment.user_id, comment.author_id))
    connection.commit()
    cursor.close()

def get_comments(poem_id):
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    query = "SELECT text,date,user_id,user.username ,user.realname FROM comment JOIN user ON comment.user_id=user.id WHERE poem_id=%s ORDER BY comment.id DESC"
    cursor.execute(query, poem_id)
    connection.commit()
    try:
        comments = cursor.fetchall()
    except:
        comments = None
    cursor.close()
    return comments

def delete_comment(id):
    cursor = connection.cursor()
    query = "DELETE FROM comment WHERE id=%s"
    cursor.execute(query, id)
    connection.commit()
    cursor.close()

def get_comments_of_author(author_id):
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    query = "SELECT text,date,user_id,user.username, user.realname FROM comment JOIN user ON comment.user_id=user.id WHERE author_id=%s ORDER BY comment.id DESC"
    cursor.execute(query, author_id)
    connection.commit()
    try:
        comments = cursor.fetchall()
    except:
        comments = None
    cursor.close()
    return comments