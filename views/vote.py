from flask import current_app, render_template, request, redirect, url_for, flash, abort
from flask_login import login_required, login_user, current_user, logout_user
from forms import VoteForm
from models.vote import Vote, add_vote, get_votes, update_vote, delete_vote
from models.poem import update_poem_avg
from models.author import update_author_avg

@login_required
def vote_add(poem_id, author_id):
    form = VoteForm()
    if not form.validate_on_submit():
        return redirect(url_for("poem_page", id=poem_id))
    point = form.data["point"]
    user_id = current_user.id
    vote = Vote(point=point, user_id=user_id, poem_id=poem_id, author_id=author_id)
    try:
        add_vote(vote)
    except:
        update_vote(vote)
    update_poem_avg(poem_id)
    update_author_avg(author_id)
    return redirect(url_for("poem_page", id=poem_id))

@login_required
def vote_delete(poem_id, author_id):
    delete_vote(poem_id, current_user.id)
    update_poem_avg(poem_id)
    update_author_avg(author_id)
    return redirect(url_for("poem_page", id=poem_id))