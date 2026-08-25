import json
import uuid
import os

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
DATA_FILE = os.path.join(DATA_DIR, "projects.json")

DEFAULT_COLUMNS = {
    "por_hacer": [],
    "en_progreso": [],
    "hecho": []
}


def _load():
    if not os.path.exists(DATA_FILE):
        return {"language": "en", "projects": []}
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    if "language" not in data:
        data["language"] = "en"
    return data


def _save(data):
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def get_projects():
    return _load()["projects"]


def get_language():
    return _load().get("language", "en")


def save_language(lang):
    data = _load()
    data["language"] = lang
    _save(data)


def get_project(project_id):
    data = _load()
    for p in data["projects"]:
        if p["id"] == project_id:
            return p
    return None


def create_project(name):
    data = _load()
    project = {
        "id": str(uuid.uuid4()),
        "name": name,
        "columns": {k: list(v) for k, v in DEFAULT_COLUMNS.items()}
    }
    data["projects"].append(project)
    _save(data)
    return project


def rename_project(project_id, new_name):
    data = _load()
    for p in data["projects"]:
        if p["id"] == project_id:
            p["name"] = new_name
            break
    _save(data)


def delete_project(project_id):
    data = _load()
    data["projects"] = [p for p in data["projects"] if p["id"] != project_id]
    _save(data)


def save_board(project_id, columns):
    data = _load()
    for p in data["projects"]:
        if p["id"] == project_id:
            p["columns"] = columns
            break
    _save(data)


def save_projects_order(projects_list):
    data = _load()
    data["projects"] = projects_list
    _save(data)
