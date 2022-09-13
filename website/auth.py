from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User, Book
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint("auth", __name__)

@auth.route("/login", methods=["GET", "POST"])
def login():
  if request.method == "POST":
    email = request.form.get("email")
    password = request.form.get("password")
    
    user = User.query.filter_by(email=email).first()
    if user:
      if check_password_hash(user.password, password):
        flash("Logged in successfully!", category="success")
        login_user(user, remember=True)
        return redirect(url_for("views.home"))
      else:
        flash("Incorrect password, try again.", category="error")
    else:
      flash("Email does not exist.", category="error")
          
  return render_template("login.html")

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))

@auth.route("/sign-up", methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        email = request.form.get("email")
        first_name = request.form.get("firstName")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        userCode = request.form.get("admin")

        user = User.query.filter_by(email=email).first()
        check = True
        access_level = 0
        if userCode:
          if not check_password_hash((open("adminhash.txt", "r")).readlines()[0], userCode):
            flash("The admin code you entered was incorrect.", category="error")
            check = False
          else:
            access_level = 1
        if user:
            flash("Email already being used by an account.", category="error")
            check = False
        elif len(email) < 4:
            flash("Email must be greater than 3 characters.", category="error")
            check = False
        elif len(first_name) < 2:
            flash("First name must be greater than 1 character.", category="error")
            check = False
        elif password1 != password2:
            flash("Passwords must match.", category="error")
            check = False
        elif len(password1) < 7:
            flash("Password must be at least 7 characters.", category="error")
            check = False
        if check:
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(password1, method="sha256"), access_level=access_level)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash("Account created!", category="success")
            return redirect(url_for("views.home"))

    return render_template("signup.html")