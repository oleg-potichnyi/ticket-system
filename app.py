from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate


app = Flask(__name__)
app.config.from_object("config.Config")

db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = "login"

if __name__ == "__main__":
    app.run(debug=True)
