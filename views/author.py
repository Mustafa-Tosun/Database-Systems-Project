from flask import render_template, request, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from forms import AuthorForm, CommentForm
from tables.author import Author, add_author, update_author, delete_author, get_author_by_id, get_authors
from tables.poem import get_poems_of_author
from tables.comment import get_comments_of_author
from tables.user import get_user_by_id
from views.comment import comment_add_author

def author_page(id):
    author = get_author_by_id(id)
    if author is None:
        abort(404)
    poems = get_poems_of_author(id)
    for poem in poems:
        #poem['text'] = poem['text'].decode('utf-8')
        poem['text'] = poem['text'].splitlines()[0:4]
    comment_form = CommentForm()
    comments = get_comments_of_author(id)
    if request.method == "GET":
        print("asdfasdf")
        return render_template("author.html", author=author, poems=poems, comment_form=comment_form, comments=comments)
    else:
        if request.form['btn'] == 'edit':
            return redirect(url_for("author_edit_page", id=id))
        if request.form['btn'] == 'submit_comment':
            comment_add_author(id)
            return redirect(url_for("author_page", id=id))
        else:
            comment_id = request.form['btn']
            print("sadfasdfasdfasdf")
            return redirect(url_for("comment_edit_page", comment_id=comment_id))

def authors_page():
    if request.method == "GET":
        authors = get_authors()
        return render_template("authors.html", authors=authors)
    else:
        if not current_user.is_admin:
            abort(401)
        form_author_ids = request.form.getlist('ids')
        if form_author_ids != None:
            for id in form_author_ids:
                print(id)
                delete_author(int(id))
        return redirect(url_for("authors_page"))


@login_required
def author_add_page():
    if not current_user.is_admin:
        abort(401)
    form = AuthorForm()
    if request.method == "GET":
        return render_template("author_add.html", form=form)
    else:
        if not form.validate_on_submit():
            return render_template("author_add.html", form=form)
        name = form.data["name"]
        birth = form.data["birth"]
        death = form.data["death"]
        author = Author(name=name, birth=birth, death=death)
        try:
            id = add_author(author)
            return redirect(url_for("author_page", id=id))
        except:
            flash("Author is already in database!", 'is-danger')
            return render_template("author_add.html", form=form)
        

@login_required
def author_edit_page(id):
    if not current_user.is_admin:
        abort(401)
    form = AuthorForm()
    if request.method == "GET":
        author = get_author_by_id(id)
        if author is None:
            abort(404)
        form.name.data = author['name']
        form.birth.data = author['birth']
        form.death.data = author['death'] 
        return render_template("author_edit.html", form=form)
    else:
        if not form.validate_on_submit():
            return render_template("author_edit.html", form=form)
        name = form.data["name"]
        birth = form.data["birth"]
        death = form.data["death"]
        author = Author(id=id, name=name, birth=birth, death=death)
        update_author(author)
        return redirect(url_for("author_page", id=id))

@login_required
def author_delete_page(id):
    if not current_user.is_admin:
        abort(401)
    delete_author(id)
    return redirect(url_for("authors_page"))