from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models import Task, User
from flask_jwt_extended import jwt_required, get_jwt_identity

task_bp = Blueprint("tasks", __name__)

# ✅ Create Task (Login required)
@task_bp.route("/", methods=["POST"])
@jwt_required()
def create_task():
    user_id = int(get_jwt_identity())   # 🔥 FIX (important)

    data = request.get_json()

    if not data or "title" not in data or "description" not in data:
        return jsonify({"msg": "Invalid data"}), 400

    task = Task(
        title=data["title"],
        description=data["description"],
        user_id=user_id
    )

    db.session.add(task)
    db.session.commit()

    return jsonify({"msg": "Task created"}), 200


# ✅ Get Tasks
# ✅ Get Tasks (Pagination + Filtering)
@task_bp.route("/", methods=["GET"])
@jwt_required()
def get_tasks():
    user_id = int(get_jwt_identity())

    # 🔹 Pagination params
    page = int(request.args.get("page", 1))
    limit = int(request.args.get("limit", 5))

    # 🔹 Filtering param
    status = request.args.get("status")

    # 🔹 Base query
    query = Task.query.filter_by(user_id=user_id)

    # 🔹 Apply filtering
    if status:
        query = query.filter_by(status=status)

    # 🔹 Apply pagination
    tasks = query.paginate(page=page, per_page=limit)

    # 🔹 Response same (important for tests)
    result = []
    for t in tasks.items:
        result.append({
            "id": t.id,
            "title": t.title,
            "status": t.status,
            "user_id": t.user_id
        })

    return jsonify(result), 200


# ✅ Assign Task
@task_bp.route("/<int:id>/assign", methods=["PUT"])
@jwt_required()
def assign_task(id):
    user_id = int(get_jwt_identity())   # 🔥 FIX
    user = User.query.get(user_id)

    if user.role != "admin":
        return jsonify({"msg": "Only admin can assign task"}), 403

    data = request.get_json()
    if not data or "user_id" not in data:
        return jsonify({"msg": "Invalid data"}), 400

    task = Task.query.get(id)
    if not task:
        return jsonify({"msg": "Task not found"}), 404

    task.user_id = data["user_id"]
    db.session.commit()

    return jsonify({"msg": "Task assigned"}), 200


# ✅ Update Task
@task_bp.route("/<int:id>", methods=["PUT"])
@jwt_required()
def update_task(id):
    user_id = int(get_jwt_identity())   # 🔥 FIX

    task = Task.query.get(id)
    if not task:
        return jsonify({"msg": "Task not found"}), 404

    data = request.get_json()
    if not data:
        return jsonify({"msg": "Invalid data"}), 400

    task.title = data.get("title", task.title)
    task.status = data.get("status", task.status)

    db.session.commit()

    return jsonify({"msg": "Task updated"}), 200


# ✅ Delete Task
@task_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_task(id):
    user_id = int(get_jwt_identity())   # 🔥 FIX
    user = User.query.get(user_id)

    if user.role != "admin":
        return jsonify({"msg": "Only admin can delete"}), 403

    task = Task.query.get(id)
    if not task:
        return jsonify({"msg": "Task not found"}), 404

    db.session.delete(task)
    db.session.commit()

    return jsonify({"msg": "Task deleted"}), 200