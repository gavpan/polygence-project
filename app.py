from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import psycopg2
import jwt
import datetime
 
app = Flask(__name__)
CORS(app)
 
# In a real app, load this from an environment variable, not a hardcoded string.
app.config["SECRET_KEY"] = "change-this-to-something-random-and-secret"
 
 
def get_db_connection():
    conn = psycopg2.connect(
        host="localhost",
        database="schedzen_db",
        user="postgres",
        password="schedzen"
    )
 
    return conn
 
 
# ---------------------------------------------------------------------------
# Auth helpers
# ---------------------------------------------------------------------------
 
def token_required(f):
    """Decorator for routes that require a valid JWT.
    Expects header: Authorization: Bearer <token>
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
 
        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({"message": "Missing or malformed token"}), 401
 
        token = auth_header.split(" ")[1]
 
        try:
            payload = jwt.decode(
                token, app.config["SECRET_KEY"], algorithms=["HS256"]
            )
            current_user_id = payload["user_id"]
        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Token has expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"message": "Invalid token"}), 401
 
        # Pass the authenticated user's id through to the route
        return f(current_user_id, *args, **kwargs)
 
    return decorated
 
 
# ---------------------------------------------------------------------------
# Auth routes
# ---------------------------------------------------------------------------
 
@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
 
    username = data.get("username")
    password = data.get("password")
 
    if not username or not password:
        return jsonify({"message": "Username and password are required"}), 400
 
    password_hash = generate_password_hash(password)
 
    conn = get_db_connection()
    cur = conn.cursor()
 
    try:
        cur.execute(
            """
            INSERT INTO credentials (username, password_hash)
            VALUES (%s, %s)
            RETURNING user_id;
            """,
            (username, password_hash)
        )
        new_user_id = cur.fetchone()[0]
        conn.commit()
    except psycopg2.errors.UniqueViolation:
        conn.rollback()
        return jsonify({"message": "Username already taken"}), 409
    finally:
        cur.close()
        conn.close()
 
    return jsonify({
        "message": "User registered successfully",
        "user_id": new_user_id
    }), 201
 
 
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
 
    username = data.get("username")
    password = data.get("password")
 
    if not username or not password:
        return jsonify({"message": "Username and password are required"}), 400
 
    conn = get_db_connection()
    cur = conn.cursor()
 
    cur.execute(
        "SELECT user_id, password_hash FROM credentials WHERE username = %s;",
        (username,)
    )
    row = cur.fetchone()
 
    cur.close()
    conn.close()
 
    if row is None:
        return jsonify({"message": "Invalid username or password"}), 401
 
    user_id, password_hash = row
 
    if not check_password_hash(password_hash, password):
        return jsonify({"message": "Invalid username or password"}), 401
 
    token = jwt.encode(
        {
            "user_id": user_id,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        },
        app.config["SECRET_KEY"],
        algorithm="HS256"
    )
 
    return jsonify({
        "message": "Login successful",
        "token": token,
        "user_id": user_id
    })
 
 
# Returns the logged-in user's own data. Requires a valid JWT.
@app.route("/profile", methods=["GET"])
@token_required
def profile(current_user_id):
    conn = get_db_connection()
    cur = conn.cursor()
 
    cur.execute(
        "SELECT user_id, username, created_at FROM credentials WHERE user_id = %s;",
        (current_user_id,)
    )
    row = cur.fetchone()
 
    cur.close()
    conn.close()
 
    if row is None:
        return jsonify({"message": "User not found"}), 404
 
    user_id, username, created_at = row
 
    # Never include password_hash here — the frontend has no reason to see it.
    return jsonify({
        "user_id": user_id,
        "username": username,
        "created_at": str(created_at)
    })
 
 
# ---------------------------------------------------------------------------
# Existing routes (unchanged)
# ---------------------------------------------------------------------------
 
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
 
 
# Add task
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
        """
        INSERT INTO tasks
        (user_id, title, due_date, estimated_time, priority)
        VALUES (%s, %s, %s, %s, %s);
        """,
        (user_id, title, due_date, estimated_time, priority)
    )
 
    conn.commit()
 
    cur.close()
    conn.close()
 
    return jsonify({
        "message": "Task added successfully"
    })
 
 
# Delete task
@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    conn = get_db_connection()
    cur = conn.cursor()
 
    cur.execute(
        "DELETE FROM tasks WHERE task_id = %s;",
        (task_id,)
    )
 
    conn.commit()
 
    cur.close()
    conn.close()
 
    return jsonify({
        "message": "Task deleted successfully"
    })
 
 
# Chatbot test endpoint
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
 
    user_message = data["message"]
 
    reply = "Test message to see if it works: " + user_message
 
    return jsonify({
        "reply": reply
    })
 
 
# Home test route
@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Flask is working"
    })
 
 
if __name__ == "__main__":
    print(app.url_map)
    app.run(debug=True)