import pymysql
from server import connection

class Poem:
    def __init__(self, title, text, author_id, year=-1, average=-1, id=""):
        self.id = id
        self.title = title
        self.text = text
        self.author_id = author_id
        self.year = year
        self.average = average

def add_poem(poem):
    cursor = connection.cursor()
    query = "INSERT INTO poem(title, text, author_id, year, average) VALUES(%s, %s, %s, %s, %s)"
    cursor.execute(query, (poem.title, poem.text, poem.author_id, poem.year, poem.average))
    connection.commit()
    query = "SELECT LAST_INSERT_ID()"
    cursor.execute(query)
    connection.commit()
    id = cursor.fetchone()
    return id[0]

def get_poem_by_id(id):
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    query = "SELECT poem.id, title, text, author_id, year, poem.average, author.name as author_name FROM poem JOIN author on author_id=author.id WHERE poem.id=%s"
    cursor.execute(query, id)
    connection.commit()
    try:
        poem = cursor.fetchone()
    except:
        poem = None
    cursor.close()
    return poem

def get_poems():
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    query = "SELECT poem.id, title, text, year, poem.average, author_id, author.name as author_name FROM poem JOIN author ON author.id=poem.author_id"
    cursor.execute(query)
    connection.commit()
    poems = cursor.fetchall()
    cursor.close()
    return poems

def update_poem(poem):
    cursor = connection.cursor()
    query = "UPDATE poem SET title=%s, text=%s, year=%s WHERE id=%s"
    cursor.execute(query, (poem.title, poem.text, poem.year, poem.id))
    connection.commit()
    cursor.close()
    return poem.id

def delete_poem(id):
    cursor = connection.cursor()
    query = "DELETE FROM poem WHERE id=%s"
    cursor.execute(query, id)
    connection.commit()
    cursor.close()

def update_poem_avg(id):
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    query = "SELECT AVG(point) FROM vote WHERE poem_id=%s"
    cursor.execute(query, id)
    connection.commit()
    average = cursor.fetchone()
    if average['AVG(point)'] == None:
        average['AVG(point)'] = -1
    query = "UPDATE poem SET average=%s WHERE id=%s"
    cursor.execute(query, (average['AVG(point)'], id))
    connection.commit()
    cursor.close()

def get_poems_of_author(author_id):
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    query = "SELECT id,title, text, average FROM poem WHERE author_id=%s"
    cursor.execute(query, author_id)
    connection.commit()
    try:
        poems = cursor.fetchall()
    except:
        poems = None
    cursor.close()
    return poems

def get_top_poems():
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    query = "SELECT poem.id, title, text, average FROM poem JOIN vote ON vote.poem_id=poem.id GROUP BY id HAVING COUNT(id)>2 ORDER BY average DESC LIMIT 5;"
    cursor.execute(query)
    connection.commit(),
    try:
        poems = cursor.fetchall()
    except:
        poems = None
    cursor.close()
    return poems

def get_newest_poems():
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    query = "SELECT id, title, text, average FROM poem ORDER BY id DESC LIMIT 5"
    cursor.execute(query)
    connection.commit()
    try:
        poems = cursor.fetchall()
    except:
        poems = None
    cursor.close()
    return poems

def get_author_id_of_poem(id):
    cursor = connection.cursor()
    query = "SELECT author_id FROM poem WHERE id=%s"
    cursor.execute(query, id)
    connection.commit()
    try:
        author_id = cursor.fetchone()
    except:
        author_id = None
    cursor.close()
    return author_id

def check_author_poem(author_id, poem_title):
    cursor = connection.cursor()
    query = "SELECT id FROM poem WHERE author_id=%s AND title=%s"
    cursor.execute(query, (author_id, poem_title))
    try:
        poem_id = cursor.fetchone()
    except:
        poem_id = None
    cursor.close()
    return poem_id