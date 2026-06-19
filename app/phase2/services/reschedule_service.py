import json
import os
from threading import Lock

STORE = "phase2/storage/pending_requests.json"
_lock = Lock()


def _load():
    if not os.path.exists(STORE):
        return []
    with open(STORE) as f:
        return json.load(f)


def _save(data):
    os.makedirs(os.path.dirname(STORE), exist_ok=True)
    with open(STORE, "w") as f:
        json.dump(data, f, indent=2)


def add_request(req: dict):
    with _lock:
        data = _load()
        req["request_id"] = (max([r["request_id"] for r in data], default=0) + 1)
        req["status"] = "pending"
        data.append(req)
        _save(data)
        return req


def list_requests(status: str = None):
    data = _load()
    return [r for r in data if status is None or r["status"] == status]


def update_status(request_id: int, status: str):
    with _lock:
        data = _load()
        for r in data:
            if r["request_id"] == request_id:
                r["status"] = status
                _save(data)
                return r
    return None
