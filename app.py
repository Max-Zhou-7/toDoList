from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
import json
import sqlite3

app = Flask(__name__)

items = []
finished = []
@app.route("/")
def index():
    return render_template("index.html", tasks = items, finished = finished)

@app.route("/add", methods = ['post'])
def create():
    task = request.form.get("task")
    if (task == ""):
        flash("Input cannot be empty!!!")
    items.append(task)
    #json_items = json.dumps(items)
    return redirect("/")

@app.route("/delete/<int:task_id>")
def delete(task_id):
    direction = request.args.get('direction')
    if direction == "done":
        if 0 <= task_id < len(items):
            items.pop(task_id)
    elif direction == "back":
        if 0 <= task_id < len(finished):
            finished.pop(task_id)
    return redirect(url_for("index"))



@app.route("/move/<int:task_id>", methods= ['post'])
def move(task_id):
    direction = request.args.get('direction')
    print(direction)
    if direction == "done":
        if 0 <= task_id < len(items):
            # Move task from items to finished
            task = items[task_id]
            finished.append(task)
            items.pop(task_id)
    elif direction == "back":
        if 0 <= task_id < len(finished):
            # Move task from finished to finished
            task = finished[task_id]
            items.append(task)
            finished.pop(task_id)
    return redirect("/")

@app.route('/submit', methods=['POST'])
def storage():
    print("in")
    data = request.get_json()
    undone_item = data.get("items", [])
    done_item = data.get("finished", [])
    with open('data.txt','a') as f:
        f.write("Undone: " + json.dumps(undone_item) + '\n')
        f.write("Done: " + json.dumps(done_item) + '\n')
    return jsonify({'message':'it worked!'}), 200

# # define a databasae
# def init_db():
#     conn = sqlite3.connect('database.db')
#     c = conn.cursor()
    
if __name__ == "__main__":
    app.run()