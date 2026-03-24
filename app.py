from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/tasks", methods=["GET"])
def get_tasks():
    tasks = []

    task1 = {
        "task_id": 1,
        "title": "Math homework",
        "due_date": "2026-03-29",
        "priority": "High"
    }

    task2 = {
        "task_id": 2,
        "title": "English homework",
        "due_date": "2026-03-30",
        "priority": "Medium"
    }

    tasks.append(task1)
    tasks.append(task2)

    return jsonify(tasks)

@app.route("/tasks", methods=["POST"])
def add_task():
    data = request.get_json()
    print("Received task:", data)

    return jsonify({
        "message": "Task added"
    })

@app.route("/tasks/<task_id>", methods=["PUT"])
def edit_task(task_id):
    data = request.get_json()
    print("Editing task", task_id)
    print("New data:", data)

    return jsonify({
        "message": "Task updated"
    })

@app.route("/tasks/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    print("Deleting task", task_id)

    return jsonify({
        "message": "Task deleted"
    })

@app.route("/generate-schedule", methods=["POST"])
def generate_schedule():
    data = request.get_json()
    print("Generating schedule for:", data)

    schedule = []
    schedule.append("4:00 PM - Math homework")
    schedule.append("5:00 PM - Break")
    schedule.append("5:30 PM - Science project")

    return jsonify({
        "message": "Schedule generated",
        "schedule": schedule
    })

app.run(debug=True)