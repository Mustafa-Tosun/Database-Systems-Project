from flask import redirect, request, render_template, url_for, abort
from flask_login import login_required, current_user
from forms import CommentForm
from models.comment import Comment, add_comment, delete_comment, add_comment_author, get_user_id_of_comment, get_comment, update_comment
from datetime import datetime

@login_required
def comment_add(poem_id):
    form = CommentForm()
    if not form.validate_on_submit():
        return 
    text = form.data["text"]
    date = datetime.now()
    user_id = current_user.id
    comment = Comment(text=text, date=date, user_id=user_id, poem_id=poem_id)
    add_comment(comment)
    return 

@login_required
def comment_add_author(author_id):
    form = CommentForm()
    if not form.validate_on_submit():
        return
    text = form.data["text"]
    date = datetime.now()
    user_id = current_user.id
    comment = Comment(text=text, date=date, user_id=user_id, author_id=author_id)
    add_comment_author(comment)
    return

@login_required
def comment_delete(poem_id, id):
    user_id = get_user_id_of_comment(id)
    if not current_user.is_admin or current_user.id != user_id:
        abort(401)
    delete_comment(id)
    return redirect(url_for("poem_page", id=poem_id))

@login_required
def comment_delete_author(author_id, id):
    user_id = get_user_id_of_comment(id)
    if not current_user.is_admin or current_user.id != user_id:
        abort(401)
    delete_comment(id)
    return redirect(url_for("author_page", id=author_id))

@login_required
def comment_edit_page(comment_id):
    comment = get_comment(comment_id)
    if current_user.id != comment['user_id']:
        abort(401)
    form = CommentForm()
    if request.method=="GET":
        return render_template("comment_edit.html", comment=comment, form=form)
    else:
        edit_date = datetime.now()
        update_comment(form.data['text'], edit_date, comment_id)
        if comment['poem_id']:
            return redirect(url_for("poem_page", id=comment['poem_id']))
        else:
            return redirect(url_for("author_page", id = comment['author_id']))
