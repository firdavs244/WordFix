import requests, json

BASE = "http://localhost:8000/api/v1"
s = requests.Session()

r = s.post(f"{BASE}/auth/login/", json={"email": "test@wordfix.com", "password": "TestPass123!"})
token = r.json()["data"]["tokens"]["access"]
s.headers["Authorization"] = f"Bearer {token}"

# Test generate
r = s.post(f"{BASE}/tests/generate/", json={"test_type": "multiple_choice", "question_count": 3, "difficulty": "adaptive"})
d = r.json()
data = d.get("data")
print(f"type(data): {type(data)}")
if isinstance(data, list):
    print(f"data is list, length: {len(data)}")
    if data:
        print(f"First item keys: {list(data[0].keys()) if isinstance(data[0], dict) else 'not dict'}")
elif isinstance(data, dict):
    print(f"data keys: {list(data.keys())}")
    print(f"id: {data.get('id')}")
    print(f"session_id: {data.get('session_id')}")
    qs = data.get("questions", [])
    print(f"questions: {len(qs)}")
    if qs:
        print(f"q0 keys: {list(qs[0].keys())}")
print(json.dumps(d)[:1000])

# Word match
print("\n--- WORD MATCH ---")
r = s.post(f"{BASE}/games/word-match/start/")
d = r.json()
gd = d.get("data", d)
print(f"Match data keys: {list(gd.keys()) if isinstance(gd, dict) else type(gd)}")
print(json.dumps(d)[:600])

# Notifications
print("\n--- NOTIFICATIONS ---")
r = s.get(f"{BASE}/notifications/")
d = r.json()
ndata = d.get("data", [])
if isinstance(ndata, list) and ndata:
    n_id = ndata[0].get("id")
    print(f"First notif ID: {n_id}")
elif isinstance(ndata, dict):
    results = ndata.get("results", [])
    if results:
        n_id = results[0].get("id")
        print(f"First notif ID: {n_id}")
