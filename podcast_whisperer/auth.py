import functools
import sys

import click
from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from werkzeug.security import check_password_hash, generate_password_hash

from podcast_whisperer.database import get_db

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.cli.command("create-admin")
@click.argument("username")
@click.argument("password")
def create_admin(username, password):
    if not username:
        click.echo("Username cannot be empty", err=True)
        sys.exit(1)
    elif not password:
        click.echo("Password cannot be empty", err=True)
        sys.exit(1)
    else:
        get_db().create_user(username, generate_password_hash(password))
        click.echo("New admin created")


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get("user_id")

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().get_user_by_id(user_id)


@bp.route("/login", methods=("GET", "POST"))
def login():
    if request.method == "POST":
        username = request.form["username"]
        request_password = request.form["password"]

        user = get_db().get_user_by_name(username)

        # Account doesn't exist
        if not user:
            flash("Bad login")
        elif check_password_hash(user.hashed_password, request_password):
            session.clear()
            session["user_id"] = user.id
            return redirect(url_for("index"))
        # Incorrect password
        else:
            flash("Bad login")

    return render_template("auth/login.html")


@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))

        return view(**kwargs)

    return wrapped_view
