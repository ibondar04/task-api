from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.database import get_connection
from pwdlib import PasswordHash


app = FastAPI()

password_hash = PasswordHash.recommended()


# Defines the data a client must send when creating or updating a task.
class Task(BaseModel):
    title: str
    completed: bool = False


class User(BaseModel):
    username: str
    password: str


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.get("/tasks")
def get_tasks():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT id, title, completed FROM tasks")
    rows = cursor.fetchall()

    cursor.close()
    connection.close()

    tasks = [
        {"id": row[0], "title": row[1], "completed": row[2]}
        for row in rows
    ]

    return {"tasks": tasks}


@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT id, title, completed FROM tasks WHERE id = %s",
        (task_id,)
    )

    task = cursor.fetchone()

    cursor.close()
    connection.close()

    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    return {
        "id": task[0],
        "title": task[1],
        "completed": task[2]
    }


@app.put("/tasks/{task_id}")
def update_task(task_id: int, updated_task: Task):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE tasks
        SET title = %s, completed = %s
        WHERE id = %s
        RETURNING id, title, completed
        """,
        (updated_task.title, updated_task.completed, task_id)
    )

    task = cursor.fetchone()

    connection.commit()

    cursor.close()
    connection.close()

    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    return {
        "id": task[0],
        "title": task[1],
        "completed": task[2]
    }


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM tasks WHERE id = %s RETURNING id",
        (task_id,)
    )

    deleted_task = cursor.fetchone()

    connection.commit()

    cursor.close()
    connection.close()

    if deleted_task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    return {"message": "Task deleted"}


@app.post("/tasks")
def create_task(task: Task):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO tasks (title, completed)
        VALUES (%s, %s)
        RETURNING id, title, completed
        """,
        (task.title, task.completed)
    )

    new_task = cursor.fetchone()

    connection.commit()

    cursor.close()
    connection.close()

    return {
        "id": new_task[0],
        "title": new_task[1],
        "completed": new_task[2]
    }


@app.post("/users")
def create_user(user: User):
    connection = get_connection()
    cursor = connection.cursor()

    # Store a hash instead of the plain-text password.
    hashed_password = password_hash.hash(user.password)
    cursor.execute(
        """
        INSERT INTO users (username, password_hash)
        VALUES (%s, %s)
        RETURNING id, username
        """,
        (user.username, hashed_password)
    )

    new_user = cursor.fetchone()

    connection.commit()

    cursor.close()
    connection.close()

    return {
        "id": new_user[0],
        "username": new_user[1]
    }