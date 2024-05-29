from flask import render_template, flash, redirect, url_for
from flask_login import login_user, logout_user, current_user, login_required
from app import app, db
from ticket.models import User, Ticket, UserRole
from ticket.forms import LoginForm, RegistrationForm, TicketForm


@app.route("/")
@app.route("/index")
@login_required
def index():
    if current_user.is_admin():
        tickets = Ticket.query.all()
    elif current_user.is_manager() or current_user.is_analyst():
        tickets = Ticket.query.filter_by(group_id=current_user.group_id).all()
    else:
        tickets = []
    return render_template("index.html", title="Home", tickets=tickets)


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password")
            return redirect(url_for("login"))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for("index"))
    return render_template("login.html", title="Sign In", form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        user.role = UserRole.ADMIN
        db.session.add(user)
        db.session.commit()
        flash("Congratulations, you are now a registered user!")
        return redirect(url_for("login"))
    return render_template("register.html", title="Register", form=form)


@app.route("/ticket/new", methods=["GET", "POST"])
@login_required
def new_ticket():
    form = TicketForm()
    if form.validate_on_submit():
        ticket = Ticket(
            note=form.note.data,
            status=form.status.data,
            group_id=(current_user.group_id
                      if current_user.is_manager() or current_user.is_analyst()
                      else form.group_id.data),
            user_id=current_user.id
        )
        db.session.add(ticket)
        db.session.commit()
        flash("Ticket has been created!")
        return redirect(url_for("index"))
    return render_template("new_ticket.html", title="New Ticket", form=form)


@app.route("/ticket/<int:ticket_id>")
@login_required
def ticket(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)
    if (not current_user.is_admin() and
            ticket.group_id != current_user.group_id):
        flash("You do not have access to this ticket.")
        return redirect(url_for("index"))
    return render_template("ticket.html", title="Ticket", ticket=ticket)
