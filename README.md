# Simple Flask REST API

A small JSON API for managing tasks. Task data is kept in memory and resets
when the server restarts.

## Run

```powershell
.\myenv3\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python app.py
```

The API listens at `http://127.0.0.1:5000`.

## Run with Docker

```powershell
docker build -t lion-api .
docker run --rm -p 5000:5000 lion-api
```

Open `http://localhost:5000/` to see the available routes, or check
`http://localhost:5000/api/health` for the health status.

## Endpoints

| Method | Path | Description |
| --- | --- | --- |
| `GET` | `/api/health` | Check that the API is running |
| `GET` | `/api/tasks` | List all tasks |
| `POST` | `/api/tasks` | Create a task with a `title` |
| `GET` | `/api/tasks/<id>` | Get one task |
| `PATCH` | `/api/tasks/<id>` | Update `title` and/or `completed` |
| `DELETE` | `/api/tasks/<id>` | Delete a task |

Create a task by sending JSON such as `{"title":"Write the API"}` to
`POST /api/tasks`. New tasks start with `completed: false`.