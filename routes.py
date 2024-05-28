from flask import render_template, flash, redirect, url_for
from flask_login import login_user, logout_user, current_user, login_required
from app import app, db
from models import User, Ticket, Group


@app.route("/")
@app.route("/index")
@login_required
def index():
    tickets = Ticket.query.all()
    return render_template("index.html", title="Home", tickets=tickets)


@app.route("/login", methods=["GET", "POST"])
def login():
    # Handle login logic here
    return render_template("login.html", title="Sign In")


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))
