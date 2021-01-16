from server import connection
INIT_STATEMENTS= [
    """CREATE TABLE IF NOT EXISTS user (
        id INT UNSIGNED NOT NULL AUTO_INCREMENT,
        username VARCHAR(50) NOT NULL UNIQUE,
        email VARCHAR(255) NOT NULL UNIQUE,
        password VARCHAR(100) NOT NULL,
        realname VARCHAR(50),
        is_admin TINYINT,
        PRIMARY KEY (id)
    )""",
    """CREATE TABLE IF NOT EXISTS author (
        id INT UNSIGNED NOT NULL AUTO_INCREMENT,
        name VARCHAR(50) NOT NULL UNIQUE,
        description TEXT,
        birth SMALLINT,
        death SMALLINT,
        average FLOAT,
        PRIMARY KEY (id)
    )""",
    """CREATE TABLE IF NOT EXISTS poem (
        id INT UNSIGNED NOT NULL AUTO_INCREMENT,
        title VARCHAR(255) NOT NULL,
        text TEXT NOT NULL,
        year SMALLINT,
        average FLOAT,
        author_id INT UNSIGNED,
        FOREIGN KEY (author_id) REFERENCES author(id) ON DELETE CASCADE ON UPDATE CASCADE,
    PRIMARY KEY (id)
    )""",
    """CREATE TABLE IF NOT EXISTS comment (
        id INT UNSIGNED NOT NULL AUTO_INCREMENT,
        text TEXT NOT NULL,
        date DATE NOT NULL,
        user_id INT UNSIGNED NOT NULL,
        poem_id INT UNSIGNED,
        author_id INT UNSIGNED,
        FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE ON UPDATE CASCADE,
        FOREIGN KEY (poem_id) REFERENCES poem(id) ON DELETE CASCADE ON UPDATE CASCADE,
        FOREIGN KEY (author_id) REFERENCES author(id) ON DELETE CASCADE ON UPDATE CASCADE,
        PRIMARY KEY (id)
    )""",
    """CREATE TABLE IF NOT EXISTS vote (
        point TINYINT NOT NULL,
        user_id INT UNSIGNED NOT NULL,
        poem_id INT UNSIGNED NOT NULL,
        author_id INT UNSIGNED NOT NULL,
        FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE ON UPDATE CASCADE,
        FOREIGN KEY (poem_id) REFERENCES poem(id) ON DELETE CASCADE ON UPDATE CASCADE,
        FOREIGN KEY (author_id) REFERENCES author(id) ON DELETE CASCADE ON UPDATE CASCADE,
        PRIMARY KEY (user_id, poem_id)
    )""",
    """INSERT IGNORE INTO user(username, email, password, realname, is_admin) 
            VALUES("admin", "admin@gmail.com", "$pbkdf2-sha256$29000$kbI2RojxHoMQolSqdW5N6Q$G16Y2pCtj3qd2lTJ/26Lh8BOnebs2l/aQ6O9qYZJLVM", "Mustafa Tosun", "1")"""
]

def initialize():
    cursor = connection.cursor()
    for statement in INIT_STATEMENTS:
        cursor.execute(statement)
        connection.commit()
    cursor.close()

if __name__ == "__main__":
    initialize()