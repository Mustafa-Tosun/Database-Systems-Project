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
    cursor = connection.cursor()
    query = "SELECT name, birth, death, average FROM author WHERE id=%s"
    cursor.execute(query, id)
    connection.commit()
    try:
        name, birth, death, average = cursor.fetchone()
        author = Author(name=name, birth=birth, death=death, average=average, id=id)
    except:
        author = None
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
    cursor = connection.cursor()
    query = "SELECT AVG(point) FROM vote WHERE author_id=%s"
    cursor.execute(query, id)
    connection.commit()
    average = cursor.fetchone()
    if average[0] == None:
        average = -1
    query = "UPDATE author SET average=%s WHERE id=%s"
    cursor.execute(query, (average, id))
    connection.commit()
    cursor.close()

def get_top_authors():
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    query = "SELECT id, name, average FROM author WHERE average>0 ORDER BY average DESC LIMIT 5"
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
    query = "SELECT id, name, average FROM author ORDER BY id DESC LIMIT 5"
    cursor.execute(query)
    connection.commit()
    try:
        authors = cursor.fetchall()
    except:
        authors = None
    cursor.close()
    return authors