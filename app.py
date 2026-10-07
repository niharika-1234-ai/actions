from flask import Flask, jsonify, request, url_for


def create_app():
    app = Flask(__name__)
    app.extensions["tasks"] = {}

    @app.get("/")
    def index():
        return jsonify({
            "message": "Simple Flask REST API",
            "routes": [
                {"method": "GET", "url": "/api/health"},
                {"method": "GET", "url": "/api/tasks"},
                {"method": "POST", "url": "/api/tasks"},
                {"method": "GET", "url": "/api/tasks/<task_id>"},
                {"method": "PATCH", "url": "/api/tasks/<task_id>"},
                {"method": "DELETE", "url": "/api/tasks/<task_id>"},
            ],
        })

    @app.get("/api/health")
    def health():
        return jsonify({"status": "ok"})

    @app.route("/api/tasks", methods=["GET", "POST"])
    def tasks():
        task_store = app.extensions["tasks"]

        if request.method == "GET":
            return jsonify(list(task_store.values()))

        body = request.get_json(silent=True)
        if not isinstance(body, dict):
            return jsonify({"error": "Request body must be a JSON object."}), 400

        title = body.get("title")
        if not isinstance(title, str) or not title.strip():
            return jsonify({"error": "'title' must be a non-empty string."}), 400

        task_id = max(task_store, default=0) + 1
        task = {"id": task_id, "title": title.strip(), "completed": False}
        task_store[task_id] = task
        return jsonify(task), 201, {"Location": url_for("task_detail", task_id=task_id)}

    @app.route("/api/tasks/<int:task_id>", methods=["GET", "PATCH", "DELETE"])
    def task_detail(task_id):
        task_store = app.extensions["tasks"]
        task = task_store.get(task_id)
        if task is None:
            return jsonify({"error": "Task not found."}), 404

        if request.method == "GET":
            return jsonify(task)
        if request.method == "DELETE":
            del task_store[task_id]
            return "", 204

        body = request.get_json(silent=True)
        if not isinstance(body, dict) or not body:
            return jsonify({"error": "Request body must be a non-empty JSON object."}), 400

        unknown_fields = set(body) - {"title", "completed"}
        if unknown_fields:
            return jsonify({"error": "Only 'title' and 'completed' can be updated."}), 400

        if "title" in body:
            title = body["title"]
            if not isinstance(title, str) or not title.strip():
                return jsonify({"error": "'title' must be a non-empty string."}), 400

        if "completed" in body:
            if not isinstance(body["completed"], bool):
                return jsonify({"error": "'completed' must be a boolean."}), 400

        if "title" in body:
            task["title"] = body["title"].strip()
        if "completed" in body:
            task["completed"] = body["completed"]

        return jsonify(task)

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)