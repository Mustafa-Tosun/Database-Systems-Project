import pymysql
from server import connection

def add_favorite(user_id, poem_id):
    cursor = connection.cursor()
    query = "INSERT INTO favorite(user_id, poem_id) VALUES (%s, %s)"
    cursor.execute(query, (user_id, poem_id))
    connection.commit()
    cursor.close()

def delete_favorite(user_id, poem_id):
    cursor = connection.cursor()
    query = "DELETE FROM favorite WHERE user_id=%s AND poem_id=%s"
    cursor.execute(query, (user_id, poem_id))
    connection.commit()
    cursor.close()

def get_favorites(user_id):
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    query = "SELECT favorite.poem_id,poem.title,poem.year,poem.average,poem.author_id,author.name FROM favorite JOIN poem ON favorite.poem_id=poem.id JOIN author ON poem.author_id=author.id  WHERE user_id=%s"
    cursor.execute(query, user_id)
    connection.commit
    try:
        favorites = cursor.fetchall()
    except:
        favorites = None
    cursor.close()
    return favorites

def favorite_check(user_id, poem_id):
    cursor = connection.cursor()
    query = "SELECT * FROM favorite WHERE user_id=%s AND poem_id=%s"
    cursor.execute(query, (user_id, poem_id))
    favorite = cursor.fetchone()
    cursor.close()
    if favorite==None:
        return 1
    else:
        return 0