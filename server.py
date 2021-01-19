from flask import Flask
from flask_login import LoginManager

import pymysql
connection = pymysql.connect("poeticadb.cl0hfbdfwgc5.us-east-1.rds.amazonaws.com","radiohead","karmapolice","poetica")
#connection = pymysql.connect("remotemysql.com","ggSTCtvE2s","fALcClwcn5","ggSTCtvE2s" )
#connection = pymysql.connect("localhost","root","root","poetica")
import dbinit 

from views.user import home_page, login_page, register_page, logout_page, profile_page
from views.author import authors_page, author_page, author_add_page, author_edit_page, author_delete_page
from views.poem import poems_page, poem_page, poem_add_page, poem_edit_page, poem_delete_page
from views.comment import comment_delete, comment_delete_author, comment_edit_page
from views.favorite import favorite_page
from views.vote import votes_page

from tables.user import get_user_by_id

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
    app.add_url_rule("/profile", view_func=profile_page, methods=["GET", "POST"])
    
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
    #app.add_url_rule("/poems/<int:poem_id>/new-comment", view_func=comment_add, methods=["GET", "POST"])
    app.add_url_rule("/poems/<int:poem_id>/delete-comment/<int:id>", view_func=comment_delete, methods=["GET", "POST"])
    app.add_url_rule("/authors/<int:author_id>/delete-comment/<int:id>", view_func=comment_delete_author, methods=["GET", "POST"])
    app.add_url_rule("/edit-comment/<int:comment_id>", view_func=comment_edit_page, methods=["GET", "POST"])

    # Favorite
    app.add_url_rule("/favorites", view_func=favorite_page, methods=["GET", "POST"])

    # Vote
    app.add_url_rule("/votes", view_func=votes_page)

    lm.init_app(app)
    lm.login_view = "login_page"

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)