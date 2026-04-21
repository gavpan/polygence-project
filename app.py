from flask import Flask, request, jsonify
import psycopg2

app = Flask(__name__)

def get_db_connection():
    conn = psycopg2.connect(
        host="localhost",
        database="schedzen_db",
        user="postgres",
        password="quel2325"
    )
    return conn

# View tasks
@app.route("/tasks", methods=["GET"])
def get_tasks():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM tasks;")
    rows = cur.fetchall()

    tasks = []

    for row in rows:
        task = {
            "task_id": row[0],
            "user_id": row[1],
            "title": row[2],
            "due_date": str(row[3]),
            "estimated_time": row[4],
            "priority": row[5]
        }
        tasks.append(task)

    cur.close()
    conn.close()

    return jsonify(tasks)

# Add 
@app.route("/tasks", methods=["POST"])
def add_task():
    data = request.get_json()

    user_id = data["user_id"]
    title = data["title"]
    due_date = data["due_date"]
    estimated_time = data["estimated_time"]
    priority = data["priority"]

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO tasks (user_id, title, due_date, estimated_time, priority) VALUES (%s, %s, %s, %s, %s);",
        (user_id, title, due_date, estimated_time, priority)
    )

    conn.commit()

    cur.close()
    conn.close()

    return jsonify({"message": "Task added successfully"})

# Delete
@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("DELETE FROM tasks WHERE task_id = %s;", (task_id,))
    conn.commit()

    cur.close()
    conn.close()

    return jsonify({"message": "Task deleted successfully"})


if __name__ == "__main__":
    app.run(debug=True)