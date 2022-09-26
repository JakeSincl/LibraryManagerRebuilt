from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import User, Book
from . import db


views = Blueprint("views", __name__)


@views.route("/")
def welcome():
  return render_template("welcome.html")

@views.route("/home", methods=["GET", "POST"])
@login_required
def home():
  if request.method == "POST":
    if request.form['action'] == 'add_book':
      book = Book.query.filter_by(id=request.form.get("add_book")).first()
      book.loaned_to = current_user.id
      db.session.commit()
      return redirect(url_for("views.home"))
    elif request.form['action'] == 'remove_book':
      book = Book.query.filter_by(id=request.form.get("remove_book")).first()
      book.loaned_to = 0
      db.session.commit()
      return redirect(url_for("views.home"))
    else:
      book_id = request.form.get("action")
      book = Book.query.filter_by(id=book_id).first()
      return render_template("book.html", book=book)
  else:
    return render_template("home.html", allBooks=Book.query.all())

@views.route("/adminDashboard", methods=["GET", "POST"])
@login_required
def adminDashboard():
  if request.method == "POST":
    if request.form["form-name"] == "addBook":
      title = request.form.get("title")
      author = request.form.get("author")
      description = request.form.get("description")
      publish_year = int(request.form.get("publish_year"))
      if not title:
        flash("You must enter a title.", category="error")
      elif not author:
        flash("You must enter an author's name.", category="error")
      elif not description:
        flash("You must provide a description.", category="error")
      elif not publish_year:
        flash("You must enter the year in which the book was published.", category="error")
      else: 
        new_book = Book(title=title, author=author, description=description, publish_year=publish_year, currently_loaned=False, loaned_to=0)
        db.session.add(new_book)
        db.session.commit()
        flash("Book added!", category="success")
        return redirect(url_for("views.adminDashboard"))
    elif request.form["form-name"] == "removeBook":
      if request.form.get("action"):
        book_id = request.form.get('action')
        print(book_id)
        book = Book.query.filter_by(id=book_id).first()
        print("Would have deleted:", book.title)
        db.session.delete(book)
        db.session.commit()
        flash("Book removed!", category="success")
        return redirect(url_for("views.adminDashboard"))
      flash("Something went wrong, please try again.", category="error")
  else:
    return render_template("adminDashboard.html", allBooks=Book.query.all())

@views.route("/account", methods=["GET", "POST"])
@login_required
def account():
  return(render_template("account.html", user=current_user))