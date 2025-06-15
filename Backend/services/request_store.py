import json
import os
import uuid

DATA_PATH = os.path.join("data", "requests.json")

# تحميل الطلبات
def load_requests():
    if not os.path.exists(DATA_PATH):
        return []
    with open(DATA_PATH, "r") as f:
        return json.load(f)

# حفظ الطلبات
def save_requests(data):
    os.makedirs("data", exist_ok=True)
    with open(DATA_PATH, "w") as f:
        json.dump(data, f, indent=2)

# إضافة طلب
def add_request(new_data):
    requests = load_requests()
    new_data["id"] = str(uuid.uuid4())
    requests.append(new_data)
    save_requests(requests)
    return new_data

# حذف طلب
def remove_request_by_id(req_id):
    requests = load_requests()
    new_requests = [r for r in requests if r["id"] != req_id]
    if len(new_requests) == len(requests):
        return False  # لم يتم الحذف
    save_requests(new_requests)
    return True
