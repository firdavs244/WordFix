import requests, json
BASE = "http://localhost:8000/api/v1"
s = requests.Session()
r = s.post(f"{BASE}/auth/login/", json={"email": "test@wordfix.com", "password": "TestPass123!"})
token = r.json()["data"]["tokens"]["access"]
s.headers["Authorization"] = f"Bearer {token}"

r = s.post(f"{BASE}/tests/generate/", json={"test_type": "multiple_choice", "question_count": 5, "difficulty": "adaptive"})
d = r.json()
data = d.get("data", {})
session = data.get("session", {})
print("session keys:", list(session.keys()) if isinstance(session, dict) else type(session))
print("session id:", session.get("id") if isinstance(session, dict) else "N/A")
print("session str:", json.dumps(session)[:400] if isinstance(session, dict) else str(session)[:400])

# Now test answer & complete
if isinstance(session, dict):
    test_id = session.get("id")
    qs = data.get("questions", [])
    if test_id and qs:
        q = qs[0]
        qid = q.get("id")
        answer = q.get("options", [""])[0]
        print(f"\nAnswering: test_id={test_id}, qid={qid}, answer={answer}")
        r = s.post(f"{BASE}/tests/{test_id}/answer/", json={"question_id": str(qid), "answer": str(answer), "response_time_ms": 3000})
        print(f"Answer status: {r.status_code}")
        print(f"Answer body: {r.text[:300]}")
        
        r = s.post(f"{BASE}/tests/{test_id}/complete/")
        print(f"\nComplete status: {r.status_code}")
        print(f"Complete body: {r.text[:300]}")

# Also test notifications read format
print("\n--- Notifications read ---")
r = s.post(f"{BASE}/notifications/read/", json={"all": True})
print(f"Notifications read (all=True): {r.status_code} - {r.text[:200]}")
