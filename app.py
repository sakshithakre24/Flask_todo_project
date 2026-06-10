from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Create Database Table
def init_db():
    conn = sqlite3.connect("tasks.db")
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task TEXT NOT NULL
    )
    """)

    conn.commit()
    conn.close()

init_db()


@app.route("/")
def home():
    conn = sqlite3.connect("tasks.db")
    cur = conn.cursor()

    cur.execute("SELECT * FROM tasks")
    tasks = cur.fetchall()

    conn.close()

    return render_template("index.html", tasks=tasks)


@app.route("/add", methods=["POST"])
def add_task():
    task = request.form["task"]

    conn = sqlite3.connect("tasks.db")
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO tasks (task) VALUES (?)",
        (task,)
    )

    conn.commit()
    conn.close()

    return redirect("/")


@app.route("/delete/<int:id>")
def delete_task(id):
    conn = sqlite3.connect("tasks.db")
    cur = conn.cursor()

    cur.execute(
        "DELETE FROM tasks WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)