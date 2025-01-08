from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Database setup
def setup_database():
    connection = sqlite3.connect("todo.db")
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'pending'
        )
    """)
    connection.commit()
    connection.close()

setup_database()

# Add a new task
def add_task(task_description):
    connection = sqlite3.connect("todo.db")
    cursor = connection.cursor()
    cursor.execute("INSERT INTO tasks (task) VALUES (?)", (task_description,))
    connection.commit()
    connection.close()
    return f"Task '{task_description}' added to your to-do list."

# View all tasks
def view_tasks():
    connection = sqlite3.connect("todo.db")
    cursor = connection.cursor()
    cursor.execute("SELECT id, task, status FROM tasks")
    tasks = cursor.fetchall()
    connection.close()
    if tasks:
        response = "Here are your tasks:\n"
        for task in tasks:
            response += f"{task[0]}. {task[1]} [{task[2]}]\n"
        return response.strip()
    else:
        return "Your to-do list is empty."

# Mark a task as complete
def mark_task_complete(task_id):
    connection = sqlite3.connect("todo.db")
    cursor = connection.cursor()
    cursor.execute("UPDATE tasks SET status = 'complete' WHERE id = ?", (task_id,))
    connection.commit()
    rows_updated = cursor.rowcount
    connection.close()
    if rows_updated > 0:
        return f"Task ID {task_id} marked as complete."
    else:
        return f"Task ID {task_id} not found."

# Process assistant queries
def process_query(query):
    if "add task" in query.lower():
        task_description = query.lower().replace("add task", "").strip()
        if task_description:
            return add_task(task_description)
        else:
            return "Please specify a task to add."
    elif "view tasks" in query.lower():
        return view_tasks()
    elif "complete task" in query.lower():
        try:
            task_id = int(query.lower().replace("complete task", "").strip())
            return mark_task_complete(task_id)
        except ValueError:
            return "Please specify a valid task ID to complete."
    else:
        return "Sorry, I didn't understand your request."

# Web service route
@app.route("/query", methods=["POST"])
def query():
    data = request.json
    user_query = data.get("query", "")
    response = process_query(user_query)
    return jsonify({"response": response})

if __name__ == "__main__":
   app.run(host="0.0.0.0", port=5000)

   
