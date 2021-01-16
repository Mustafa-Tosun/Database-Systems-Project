from flask import Flask
from flask_login import LoginManager

import pymysql
connection = pymysql.connect("sql7.freemysqlhosting.net","sql7387357","KdlqtCZW85","sql7387357" )

import dbinit
import os


from views.user import home_page, login_page, register_page, logout_page, profile_page
from views.author import authors_page, author_page, author_add_page, author_edit_page, author_delete_page
from views.poem import poems_page, poem_page, poem_add_page, poem_edit_page, poem_delete_page
from views.comment import comment_add, comments_page, comment_delete


from models.user import get_user_by_id

lm = LoginManager()

@lm.user_loader
def load_user(user_id):
    try:
        return get_user_by_id(user_id)
    except:
        return None


def create_app():
    app = Flask(__name__)
    app.config.from_object("settings")
    # User - Home
    app.add_url_rule("/", view_func=home_page)
    app.add_url_rule("/login", view_func=login_page, methods=["GET", "POST"])
    app.add_url_rule("/register", view_func=register_page, methods=["GET", "POST"])
    app.add_url_rule("/logout", view_func=logout_page)
    app.add_url_rule("/profile/<int:id>", view_func=profile_page, methods=["GET", "POST"])
    
    # Author
    app.add_url_rule("/authors", view_func=authors_page, methods=["GET", "POST"])
    app.add_url_rule("/authors/<int:id>", view_func=author_page, methods=["GET", "POST"])
    app.add_url_rule("/authors/<int:id>/edit", view_func=author_edit_page, methods=["GET", "POST"] )    
    app.add_url_rule("/new-author", view_func=author_add_page, methods=["GET", "POST"])
    app.add_url_rule("/authors/<int:id>/delete-author", view_func=author_delete_page, methods=["GET", "POST"])

    # Poem
    app.add_url_rule("/poems", view_func=poems_page, methods=["GET", "POST"])
    app.add_url_rule("/poems/<int:id>", view_func=poem_page, methods=["GET", "POST"])
    app.add_url_rule("/poems/<int:id>/edit", view_func=poem_edit_page, methods=["GET", "POST"] )
    app.add_url_rule("/new-poem", view_func=poem_add_page, methods=["GET", "POST"])
    app.add_url_rule("/poems/<int:id>/delete-poem", view_func=poem_delete_page, methods=["GET", "POST"])


    # Comment
    app.add_url_rule("/poems/<int:poem_id>/new-comment", view_func=comment_add, methods=["GET", "POST"])
    app.add_url_rule("/poems/<int:id>", view_func=comments_page)
    app.add_url_rule("/poems/<int:poem_id>/delete-comment/<int:id>", view_func=comment_delete, methods=["GET", "POST"])

    dbinit.initialize()

    lm.init_app(app)
    lm.login_view = "login_page"

    return app

def get_port():
    return int(os.environ.get("PORT",5000))

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=get_port())