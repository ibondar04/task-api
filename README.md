# Task API

A REST API built with FastAPI and PostgreSQL for managing user-specific tasks.

## Features

- User registration
- Secure password hashing
- JWT authentication
- Create, read, update, and delete tasks
- User-specific task ownership
- Filter tasks by completion status
- PostgreSQL persistence
- Basic automated API tests

## Tech Stack

- Python
- FastAPI
- PostgreSQL
- SQL
- Psycopg2
- JWT
- Pydantic
- Pytest

## API Endpoints

### Users

- `POST /users` — Create a new user
- `POST /login` — Log in and receive a JWT access token
- `GET /users/me` — Get the currently authenticated user

### Tasks

- `GET /tasks` — Get all tasks belonging to the logged-in user
- `GET /tasks?completed=true` — Get completed tasks
- `GET /tasks?completed=false` — Get incomplete tasks
- `POST /tasks` — Create a task
- `GET /tasks/{task_id}` — Get a specific task
- `PUT /tasks/{task_id}` — Update a task
- `DELETE /tasks/{task_id}` — Delete a task

## Setup

Clone the repository:

```bash
git clone https://github.com/ibondar04/task-api.git
cd task-api