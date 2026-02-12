import requests, json
BASE = "http://localhost:8000/api/v1"
s = requests.Session()
r = s.post(f"{BASE}/auth/login/", json={"email": "test@wordfix.com", "password": "TestPass123!"})
token = r.json()["data"]["tokens"]["access"]
s.headers["Authorization"] = f"Bearer {token}"

r = s.post(f"{BASE}/tests/generate/", json={"test_type": "multiple_choice", "question_count": 5, "difficulty": "adaptive"})
d = r.json()
data = d.get("data", {})
if isinstance(data, dict):
    print("KEYS:", list(data.keys()))
    print("id:", data.get("id"))
    print("session_id:", data.get("session_id"))
    qs = data.get("questions", [])
    print("Qs:", len(qs))
    if qs:
        print("Q0 keys:", list(qs[0].keys()))
        print("Q0:", json.dumps(qs[0])[:300])
elif isinstance(data, list):
    print("LIST len:", len(data))
    if data:
        print("item keys:", list(data[0].keys()))
        print("item0:", json.dumps(data[0])[:300])
else:
    print("data type:", type(data))
    print("full:", json.dumps(d)[:500])
