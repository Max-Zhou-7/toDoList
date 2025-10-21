from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

# Use in-memory storage (note: resets on each serverless function call)
items = []
finished = []

@app.route("/")
@app.route("/api")
@app.route("/api/index")
def index():
    # Return simple HTML directly instead of using templates
    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta name="viewport" content="initial-scale=1, width=device-width">
        <title>ToDoList</title>
    </head>
    <body>
        <h1>Task List:</h1>
        <ul>
            {''.join([f'<li>{task} <form action="/api/move/{i}?direction=done" method="post" style="display: inline;"><button type="submit">Done</button></form> <a href="/api/delete/{i}?direction=done"><button>Delete</button></a></li>' for i, task in enumerate(items)])}
        </ul>
        
        <form action="/api/add" method="post">
            <input autocomplete="off" autofocus name="task" placeholder="Type and hit enter to add" type="text">
        </form>

        <h1>Done List:</h1>
        <ul>
            {''.join([f'<li>{item} <form action="/api/move/{i}?direction=back" method="post" style="display: inline;"><button type="submit">Back</button></form> <a href="/api/delete/{i}?direction=back"><button>Delete</button></a></li>' for i, item in enumerate(finished)])}
        </ul>
    </body>
    </html>
    """
    return html

@app.route("/api/add", methods=['POST'])
def create():
    task = request.form.get("task")
    if task and task != "":
        items.append(task)
    return redirect("/")

@app.route("/api/delete/<int:task_id>")
def delete(task_id):
    direction = request.args.get('direction')
    if direction == "done" and 0 <= task_id < len(items):
        items.pop(task_id)
    elif direction == "back" and 0 <= task_id < len(finished):
        finished.pop(task_id)
    return redirect("/")

@app.route("/api/move/<int:task_id>", methods=['POST'])
def move(task_id):
    direction = request.args.get('direction')
    if direction == "done" and 0 <= task_id < len(items):
        task = items[task_id]
        finished.append(task)
        items.pop(task_id)
    elif direction == "back" and 0 <= task_id < len(finished):
        task = finished[task_id]
        items.append(task)
        finished.pop(task_id)
    return redirect("/")