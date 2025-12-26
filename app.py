from flask import Flask, render_template, request
from database import get_db_connection, init_db

app = Flask(__name__)
init_db()

@app.route("/")
def index():
    conn = get_db_connection()
    tasks = conn.execute("SELECT * FROM tasks").fetchall()
    conn.close()
    return render_template("index.html", tasks=tasks)


@app.route("/add-task", methods=["POST"])
def add_task():
    task = request.form.get("task")

    if task:
        conn = get_db_connection()
        conn.execute(
            "INSERT INTO tasks (title, completed) VALUES (?, 0)",
            (task,)
        )
        conn.commit()

        tasks = conn.execute("SELECT * FROM tasks").fetchall()
        conn.close()

        return render_template("task_list.html", tasks=tasks)


@app.route("/delete-task/<int:id>", methods=["POST"])
def delete_task(id):
    conn = get_db_connection()
    conn.execute("DELETE FROM tasks WHERE id = ?", (id,))
    conn.commit()

    tasks = conn.execute("SELECT * FROM tasks").fetchall()
    conn.close()

    return render_template("task_list.html", tasks=tasks)


@app.route("/toggle-task/<int:id>", methods=["POST"])
def toggle_task(id):
    conn = get_db_connection()

    conn.execute("""
        UPDATE tasks
        SET completed = CASE completed
            WHEN 0 THEN 1
            ELSE 0
        END
        WHERE id = ?
    """, (id,))

    conn.commit()

    tasks = conn.execute("SELECT * FROM tasks").fetchall()
    conn.close()

    return render_template("task_list.html", tasks=tasks)


if __name__ == "__main__":
    app.run()
