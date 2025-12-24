from flask import Flask, render_template, request
app = Flask(__name__)
tasks=[] #temporary in-memory storage

@app.route("/")
def index():
    return render_template("index.html",tasks=tasks)

@app.route("/add-task", methods=["post"])
def add_task():
    task = request.form.get("task")
    if task:
        tasks.append(task)
    return render_template("task_list.html", tasks=tasks)
@app.route("/delete-task/<int:index>", methods=["POST"])
def delete_task(index):
    if 0 <= index < len(tasks):
        tasks.pop(index)
    return render_template("task_list.html", tasks=tasks)

if __name__ == "__main__":
    app.run(debug=True)