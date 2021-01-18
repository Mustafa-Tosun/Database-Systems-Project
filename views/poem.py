from flask import current_app, render_template, request, redirect, url_for, flash, abort
from flask_login import login_required, login_user, current_user, logout_user
from forms import PoemForm, CommentForm, VoteForm
from models.poem import Poem, add_poem, get_poem_by_id, get_poems, update_poem, delete_poem, get_author_id_of_poem, check_author_poem
from models.author import get_author_by_name, get_author_by_id, get_authors, update_author_avg
from models.user import get_user_by_id
from models.vote import get_votes, get_vote
from models.favorite import add_favorite, favorite_check, delete_favorite
from views.comment import comment_add, comments_page
from views.vote import vote_add, vote_delete

def poem_page(id):
    poem = get_poem_by_id(id)
    if poem is None:
        abort(404)
    #poem.text = poem.text.decode('utf-8')
    poem.text = poem.text.split('\n')
    comment_form = CommentForm()
    vote_form = VoteForm()
    comments = comments_page(id)
    author = get_author_by_id(poem.author_id)
    if comments != None:
        users = []
        for comment in comments:
            #comment['text'] = comment['text'].decode('utf-8')
            user = get_user_by_id(comment['user_id'])
            comment['username'] = user.username
            comment['realname'] = user.realname
    if request.method == "GET":
        if current_user.is_authenticated:
            vote = get_vote(user_id=current_user.id, poem_id=id)
        else:
            vote = None
        check = favorite_check(current_user.id, id)
        return render_template("poem.html", poem=poem, comment_form=comment_form, comments=comments, vote_form=vote_form, vote=vote, author=author, check=check)
    else:
        if request.form['btn'] == 'edit':
            return redirect(url_for("poem_edit_page", id=id))
        if request.form['btn'] == 'submit_comment':
            comment_add(id)
        if request.form['btn'] == 'submit_vote':
            vote_add(id, poem.author_id)
        if request.form['btn'] == 'delete_vote':
            vote_delete(id, poem.author_id)
        if request.form['btn'] == 'favorite':
            flash("Poem added to your favorites.")
            add_favorite(current_user.id, id)
        if request.form['btn'] == 'remove_favorite':
            flash("Poem removed from your favorites.")
            delete_favorite(current_user.id, id)
        return redirect(url_for("poem_page", id=id))

def poems_page():
    if request.method == "GET":
        poems = get_poems()
        for poem in poems:
            author = get_author_by_id(poem['author_id'])
            poem['author'] = author.name
        return render_template("poems.html", poems=poems)
    else:
        if not current_user.is_admin:
            abort(401)
        form_author_id = request.form.get("ids")
        delete_poem(form_poem_id)
        return redirect(url_for("poems_page"))

@login_required
def poem_add_page():
    if not current_user.is_admin:
        abort(401)
    form = PoemForm()
    if request.method == "GET":
        authors = get_authors()
        return render_template("poem_add.html", form=form, authors=authors)
    else:
        if not form.validate_on_submit():
            return render_template("poem_add.html", form=form)
        title = form.data["title"]
        text = form.data["text"]
        year = form.data["year"]
        author_name = form.data["author"]
        author_id = get_author_by_name(author_name)
        if(author_id == None):
            flash("Check author name!", 'is-danger')
            return render_template("poem_add.html", form=form)
        check = check_author_poem(author_id, title)
        if check:
            flash("Poem is already in database!", 'is-danger')
            return render_template("poem_add.html", form=form)
        poem = Poem(title=title, text=text, author_id=author_id, year=year)
        id = add_poem(poem)
        return redirect(url_for("poem_page", id=id))


@login_required
def poem_edit_page(id):
    if not current_user.is_admin:
        abort(401)
    form = PoemForm()
    if request.method == "GET":
        poem = get_poem_by_id(id)
        if poem is None:
            abort(404)
        form.title.data = poem.title
        form.text.data = poem.text
        form.year.data = poem.year
        author = get_author_by_id(poem.author_id)
        form.author.data = author.name
        authors = get_authors()
        return render_template("poem_edit.html", form=form, authors=authors)
    else:
        if not form.validate_on_submit():
            return render_template("poem_edit.html", form=form)
        title = form.data["title"]
        text = form.data["text"]
        year = form.data["year"]
        author_name = form.data["author"]
        author_id = get_author_by_name(author_name)
        poem = Poem(id=id, title=title, text=text, author_id=author_id, year=year)
        update_poem(poem)
        return redirect(url_for("poem_page", id=id))

@login_required
def poem_delete_page(id):
    if not current_user.is_admin:
        abort(401)
    author_id = get_author_id_of_poem(id)
    delete_poem(id) 
    update_author_avg(author_id)
    return redirect(url_for("poems_page"))