from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager, current_user
from werkzeug.security import generate_password_hash
#from flask_socketio import SocketIO, emit

db = SQLAlchemy(session_options={"autoflush": False})
DB_NAME = "database.db"

def create_app():
  app = Flask(__name__)
  app.config['SECRET_KEY'] = "THISISVERYSECRET"
  app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_NAME}"
  db.init_app(app)
  #socket = SocketIO(app)

  from .views import views
  from .auth import auth

  app.register_blueprint(views, url_prefix="/")
  app.register_blueprint(auth, url_prefix="/")

  from .models import User

  create_database(app)
  create_adminHash()
  
  login_manager = LoginManager()
  login_manager.login_view = 'auth.login'
  login_manager.init_app(app)

  

  @login_manager.user_loader
  def load_user(id):
    return User.query.get(int(id))


  @app.context_processor
  def inject_user():
    user_details = dict(user=current_user)
    if current_user.is_authenticated:
      user_details.update(access_level=current_user.access_level)
    return user_details

  return app

def create_database(app):
  if not path.exists("website/" + DB_NAME):
    db.create_all(app=app)
    print("Created Database")

def create_adminHash():
  if not path.exists("website/adminhash.txt"):
    with open("adminhash.txt", "w") as file:
      file.write(generate_password_hash("admin", method="sha256"))

