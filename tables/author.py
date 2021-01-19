import pymysql
from server import connection
class Author:
    def __init__(self, name, birth=-1, death=-1, average=-1, id=""):
        self.id = id
        self.name = name
        self.birth = birth 
        self.death = death
        self.average = average

def add_author(author):
    cursor = connection.cursor()
    query = "INSERT INTO author(name, birth, death, average) VALUES(%s, %s, %s, %s)"
    cursor.execute(query, (author.name, author.birth, author.death, author.average))
    connection.commit()
    query = "SELECT LAST_INSERT_ID()"
    cursor.execute(query)
    connection.commit()
    id = cursor.fetchone()
    cursor.close()
    return id[0]

def get_author_by_id(id):
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    query = "SELECT id, name, birth, death, average, total_votes FROM author WHERE id=%s"
    cursor.execute(query, id)
    connection.commit()
    author = cursor.fetchone()
    cursor.close()
    return author

def get_author_by_name(name):
    cursor = connection.cursor()
    query = "SELECT id FROM author WHERE name=%s"
    cursor.execute(query, name)
    connection.commit()
    id = cursor.fetchone()
    cursor.close()
    return id

def get_authors():
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    query = "SELECT * FROM author"
    cursor.execute(query)
    connection.commit()
    authors = cursor.fetchall()
    cursor.close()
    return authors

def update_author(author):
    cursor = connection.cursor()
    query = "UPDATE author SET name=%s, birth=%s, death=%s WHERE id=%s"
    cursor.execute(query, (author.name, author.birth, author.death, author.id))
    connection.commit()
    cursor.close()
    return author.id

def delete_author(id):
    cursor = connection.cursor()
    query = "DELETE FROM author WHERE id=%s"
    cursor.execute(query, id)
    connection.commit()
    cursor.close()

def update_author_avg(id):
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    query = "SELECT ROUND(AVG(point),2), COUNT(point) FROM vote WHERE author_id=%s"
    cursor.execute(query, id)
    connection.commit()
    result = cursor.fetchone()
    if result['ROUND(AVG(point),2)'] == None:
        result['ROUND(AVG(point),2)'] = -1
    query = "UPDATE author SET average=%s, total_votes=%s WHERE id=%s"
    cursor.execute(query, (result['ROUND(AVG(point),2)'], result['COUNT(point)'], id))
    connection.commit()
    cursor.close()

def get_top_authors():
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    query = "SELECT id, name, average, total_votes FROM author JOIN vote ON vote.author_id=author.id HAVING COUNT(id)>2 ORDER BY average DESC LIMIT 5"
    cursor.execute(query)
    connection.commit()
    try:
        authors = cursor.fetchall()
    except:
        authors = None
    cursor.close()
    return authors

def get_newest_authors():
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    query = "SELECT id, name, average, total_votes FROM author ORDER BY id DESC LIMIT 5"
    cursor.execute(query)
    connection.commit()
    try:
        authors = cursor.fetchall()
    except:
        authors = None
    cursor.close()
    return authors