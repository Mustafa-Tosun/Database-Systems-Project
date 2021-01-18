from flask import current_app, render_template, request, redirect, url_for, flash, abort, session
from flask_login import login_required, login_user, current_user
from models.favorite import get_favorites

@login_required
def favorite_page():
    favorites = get_favorites(current_user.id)
    return render_template("favorites.html", favorites=favorites)