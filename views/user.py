from datetime import datetime
from flask import current_app, render_template, request, redirect, url_for, flash
from flask_login import login_required, login_user, current_user, logout_user
from models.user import User, add_user, get_user_by_email, update_user, delete_user
from models.poem import get_top_poems, get_newest_poems
from models.author import get_top_authors, get_newest_authors
from forms import LoginForm, RegisterForm, UpdateUserForm
from passlib.hash import pbkdf2_sha256 as hasher


def home_page():
    today = datetime.today()
    day_name = today.strftime("%A")
    top_poems = get_top_poems()
    for poem in top_poems:
        #poem['text'] = poem['text'].decode('utf-8')
        poem['text'] = poem['text'].splitlines()[0:4]
    newest_poems = get_newest_poems()
    for poem in newest_poems:
        #poem['text'] = poem['text'].decode('utf-8')
        poem['text'] = poem['text'].splitlines()[0:4]
    top_authors = get_top_authors()
    newest_authors = get_newest_authors()
    return render_template("home.html", day=day_name, top_poems=top_poems, newest_poems=newest_poems, top_authors=top_authors, newest_authors=newest_authors)

def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.data["email"]
        user = get_user_by_email(email)
        if user is not None:
            password = form.data["password"]
            if hasher.verify(password, user.password):
                login_user(user)
                flash("You have logged in.")
                next_page = request.args.get("next", url_for("home_page"))
                return redirect(next_page)
        flash("Invalid credentials. Check email and password!")
    return render_template("login.html", form=form)

def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        email1 = form.data["email1"]
        email2 = form.data["email2"]
        if email1 == email2:
            password1 = form.data["password1"]
            password2 = form.data["password2"]
            if password1 == password2:
                password = hasher.hash(password1)
                username = form.data['username']
                realname = form.data['realname']
                user = User(email1, password, username, realname)
                add_user(user)
                flash("Registered successfully.")
                return redirect(url_for("login_page"))
            else: flash("Passwords are not same!")
        else: flash("Emails are not same!")
    return render_template("register.html", form=form)

@login_required
def logout_page():
    logout_user()
    flash("You have logged out.")
    return redirect(url_for("home_page"))

@login_required
def profile_page(id):
    form = UpdateUserForm()
    if request.method == "GET":
        return render_template("profile.html", form=form)
    else:
        if request.form['btn'] == 'submit_change':
            if not form.validate_on_submit():
                return render_template("profile.html", form=form)
            realname = form.data["realname"]
            update_user(id, realname)
            flash("Change is saved.")
            return redirect(url_for("profile_page", id=id))
        else:
            if current_user.is_admin:
                flash("Administrator accounts can not be deleted!")
                return redirect(url_for("profile_page", id=id))
            logout_user()
            delete_user(id)
            flash("Your account is deleted.")
            return redirect(url_for("home_page"))