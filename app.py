from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_object("config.Config")

db = SQLAlchemy(app)
login = LoginManager(app)
login.login_view = "login"

# Import the models after initializing db to avoid circular imports
from models import Ticket, User, Group


@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


if __name__ == "__main__":
    app.run(debug=True)
