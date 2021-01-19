from flask import render_template, request, redirect, url_for
from flask_login import login_required, current_user
from tables.favorite import get_favorites, delete_favorite

@login_required
def favorite_page():
    if request.method == "GET":
        favorites = get_favorites(current_user.id)
        return render_template("favorites.html", favorites=favorites)
    else:
        form_poem_ids = request.form.getlist("poem_ids")
        for form_poem_id in form_poem_ids:
            delete_favorite(current_user.id, form_poem_id)
        return redirect(url_for("favorite_page"))