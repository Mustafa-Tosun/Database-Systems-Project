import pymysql
from server import connection
class Vote:
    def __init__(self, point, user_id, poem_id, author_id):
        self.point = point
        self.user_id = user_id
        self.poem_id = poem_id
        self.author_id = author_id

def add_vote(vote):
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    query = "INSERT INTO vote(point, user_id, poem_id, author_id) VALUES (%s, %s, %s, %s)"
    cursor.execute(query, (vote.point, vote.user_id, vote.poem_id, vote.author_id))
    connection.commit()
    cursor.close()

def update_vote(vote):
    cursor = connection.cursor()
    query = "UPDATE vote SET point=%s WHERE user_id=%s AND poem_id=%s"
    cursor.execute(query, (vote.point, vote.user_id, vote.poem_id))
    connection.commit()
    cursor.close()

def get_votes(poem_id):
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    query = "SELECT vote WHERE poem_id=%s"
    cursor.execute(query, poem_id)
    connection.commit()
    votes = cursor.fetchall()
    cursor.close()
    return votes

def get_vote(user_id, poem_id):
    cursor = connection.cursor()
    query = "SELECT point FROM vote WHERE user_id=%s AND poem_id=%s"
    cursor.execute(query, (user_id, poem_id))
    connection.commit()
    try:
        result = cursor.fetchone()
        point = result[0]
    except:
        point = None
    cursor.close()
    return point

def delete_vote(poem_id, user_id):
    cursor = connection.cursor()
    query = "DELETE FROM vote WHERE user_id=%s AND poem_id=%s"
    try:
        cursor.execute(query, (user_id, poem_id))
        connection.commit()
        cursor.close()
    except:
        cursor.close()
    return