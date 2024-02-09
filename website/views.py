from flask import Blueprint, redirect, render_template, url_for, request
from .models import Todo
from . import db
from datetime import datetime

my_view = Blueprint("my_view", __name__)

@my_view.route("/")
def home():
    try:
        todo_list = Todo.query.all()#
        message_type = request.args.get("message_type", None)
        message = request.args.get("message", None)
        # message_type = "success"
        # message = "Home loaded successfully."
        return render_template("page1.html", todo_list=todo_list, message=message, message_type=message_type )
    except:
        message_type = "error"
        message = "An error occurred while loading the home page."
        return render_template("page1.html", message=message, message_type=message_type)

@my_view.route("/add", methods=["POST"])
def add():
    try:
        task = request.form.get("task")
        new_todo = Todo(task=task, date_created=datetime.utcnow())
        db.session.add(new_todo)
        db.session.commit()
        message_type = "success"
        message = "Task added successfully."
        return redirect(url_for("my_view.home", message=message, message_type=message_type))
    except:
        message_type = "error"
        message = "An error occurred while adding a task."
        return redirect(url_for("my_view.home", message=message, message_type=message_type))

# @my_view.route("/update/<todo_id>")
# def update(todo_id):
#     todo = Todo.query.filter_by(id=todo_id).first()
#     todo.complete = not todo.complete
#     db.session.commit()
#     return redirect(url_for("my_view.home"))

@my_view.route("/edit/<todo_id>", methods=["POST"])
def edit(todo_id):
    try:
        todo = Todo.query.filter_by(id=todo_id).first()
        edited_task = request.form.get("edit_task")
        todo.task = edited_task
        db.session.commit()
        message_type = "success"
        message = "Task edited successfully."
        return redirect(url_for("my_view.home", message=message, message_type=message_type))
    except:
        message_type = "error"
        message = "An error occurred while editing a task."
        return redirect(url_for("my_view.home", message=message, message_type=message_type))

@my_view.route("/toggle/<todo_id>", methods=["POST"])
def toggle(todo_id):
    try:
        todo = Todo.query.get(todo_id)
        todo.complete = not todo.complete
        db.session.commit()
        message_type = "success"
        message = "Task toggled successfully."
        return redirect(url_for("my_view.home", message=message, message_type=message_type))
    except:
        message_type = "error"
        message = "An error occurred while toggling a task."
        return redirect(url_for("my_view.home", message=message, message_type=message_type))

@my_view.route("/delete/<todo_id>")
def delete(todo_id):
    try:
        todo = Todo.query.filter_by(id=todo_id).first()
        db.session.delete(todo)
        db.session.commit()
        message_type = "success"
        message = "Task deleted successfully."
        return redirect(url_for("my_view.home", message=message, message_type=message_type))
    except:
        message_type = "error"
        message = "An error occurred while deleting a task."
        return redirect(url_for("my_view.home", message=message, message_type=message_type))