from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    BooleanField,
    SubmitField,
    TextAreaField,
    SelectField
)
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from ticket.models import User, TicketStatus, Group


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Sign In")


class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    password2 = PasswordField(
        "Repeat Password", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Register")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError("Please use a different username.")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError("Please use a different email address.")


class TicketForm(FlaskForm):
    note = TextAreaField("Note", validators=[DataRequired()])
    status = SelectField(
        "Status",
        choices=TicketStatus.choices,
        validators=[DataRequired()]
    )
    group_id = SelectField("Group", coerce=int, validators=[DataRequired()])
    submit = SubmitField("Create Ticket")

    def __init__(self, *args, **kwargs):
        super(TicketForm, self).__init__(*args, **kwargs)
        self.group_id.choices = [
            (group.id, group.name) for group in Group.query.all()
        ]
