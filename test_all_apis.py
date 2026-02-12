"""
Comprehensive API testing script.
Run inside Docker: docker compose exec web python /app/test_all_apis.py
"""
import json
import sys
import requests

BASE = "http://localhost:8000/api/v1"
s = requests.Session()

errors = []
successes = []


def test(name, r, expected=None):
    expected = expected or [200, 201, 202, 204]
    if r.status_code in expected:
        successes.append(f"OK {name}: {r.status_code}")
        print(f"  ✓ {name}: {r.status_code}")
    else:
        msg = f"FAIL {name}: {r.status_code} - {r.text[:300]}"
        errors.append(msg)
        print(f"  ✗ {msg}")
    return r


# ══════════════════════════════════════════════════
# A) AUTH
# ══════════════════════════════════════════════════
print("\n=== A) AUTH ===")
r = s.post(f"{BASE}/auth/login/", json={"email": "test@wordfix.com", "password": "TestPass123!"})
test("POST /auth/login/", r)
if r.status_code == 200:
    data = r.json()
    token = data["data"]["tokens"]["access"]
    s.headers["Authorization"] = f"Bearer {token}"
    print(f"  Token obtained successfully")
else:
    print("FATAL: Cannot login, aborting")
    sys.exit(1)

r = s.get(f"{BASE}/auth/profile/")
test("GET /auth/profile/", r)

# Wrong password test
r2 = requests.post(f"{BASE}/auth/login/", json={"email": "test@wordfix.com", "password": "wrong"})
test("POST /auth/login/ (wrong pass)", r2, [401, 400])

# ══════════════════════════════════════════════════
# B) WORDS
# ══════════════════════════════════════════════════
print("\n=== B) WORDS ===")
r = s.get(f"{BASE}/words/")
test("GET /words/", r)
if r.status_code == 200:
    wd = r.json()
    data_field = wd.get("data", wd)
    if isinstance(data_field, list):
        results = data_field
    elif isinstance(data_field, dict):
        results = data_field.get("results", [])
    else:
        results = []
    print(f"  Words count: {len(results)}")

r = s.get(f"{BASE}/words/?search=abandon")
test("GET /words/?search=abandon", r)

r = s.get(f"{BASE}/words/?difficulty_level=hard")
test("GET /words/?difficulty_level=hard", r)

r = s.get(f"{BASE}/words/stats/")
test("GET /words/stats/", r)
if r.status_code == 200:
    print(f"  Stats: {json.dumps(r.json(), indent=2)[:300]}")

r = s.get(f"{BASE}/words/categories/")
test("GET /words/categories/", r)

# Get a word ID
r = s.get(f"{BASE}/words/")
word_id = None
word_ids = []
if r.status_code == 200:
    wd = r.json()
    data_field = wd.get("data", wd)
    if isinstance(data_field, list):
        results = data_field
    elif isinstance(data_field, dict):
        results = data_field.get("results", [])
    else:
        results = []
    if results:
        word_id = results[0].get("id")
        word_ids = [w.get("id") for w in results[:5]]

if word_id:
    r = s.get(f"{BASE}/words/{word_id}/")
    test(f"GET /words/{{id}}/", r)

# POST new word
r = s.post(f"{BASE}/words/", json={
    "original_word": "temporary_test_word",
    "translation": "vaqtinchalik",
    "difficulty_level": "easy",
    "part_of_speech": "adjective"
})
test("POST /words/", r, [200, 201])
new_word_id = None
if r.status_code in [200, 201]:
    new_word_id = r.json().get("data", r.json()).get("id")

# PATCH
if new_word_id:
    r = s.patch(f"{BASE}/words/{new_word_id}/", json={"translation": "vaqtinchalik test"})
    test(f"PATCH /words/{{id}}/", r)

# DELETE
if new_word_id:
    r = s.delete(f"{BASE}/words/{new_word_id}/")
    test(f"DELETE /words/{{id}}/", r, [200, 204])

# Bulk create
r = s.post(f"{BASE}/words/bulk/", json={
    "words": [
        {"original_word": "temp_bulk_1", "translation": "test1", "difficulty_level": "easy"},
        {"original_word": "temp_bulk_2", "translation": "test2", "difficulty_level": "medium"},
        {"original_word": "temp_bulk_3", "translation": "test3", "difficulty_level": "hard"},
    ]
})
test("POST /words/bulk/", r, [200, 201])

# Clean up bulk words
for w in ["temp_bulk_1", "temp_bulk_2", "temp_bulk_3"]:
    rr = s.get(f"{BASE}/words/?search={w}")
    if rr.status_code == 200:
        df = rr.json().get("data", rr.json())
        results = df if isinstance(df, list) else df.get("results", []) if isinstance(df, dict) else []
        for rw in results:
            if rw.get("original_word") == w:
                s.delete(f"{BASE}/words/{rw['id']}/")

# ══════════════════════════════════════════════════
# C) REVIEW
# ══════════════════════════════════════════════════
print("\n=== C) REVIEW ===")
r = s.get(f"{BASE}/review/words/")
test("GET /review/words/", r)

r = s.get(f"{BASE}/review/summary/")
test("GET /review/summary/", r)

r = s.get(f"{BASE}/review/streak/")
test("GET /review/streak/", r)

r = s.get(f"{BASE}/review/daily-progress/")
test("GET /review/daily-progress/", r)

# Start session
r = s.post(f"{BASE}/review/sessions/", json={"session_type": "review", "word_count": 5})
test("POST /review/sessions/", r, [200, 201])
session_id = None
if r.status_code in [200, 201]:
    sd = r.json().get("data", r.json())
    session_id = sd.get("id") or sd.get("session_id")
    review_words = sd.get("words", [])
    print(f"  Session: {session_id}, words: {len(review_words)}")

# Answer
if session_id and word_ids:
    for i, quality in enumerate([0, 2, 3, 4, 5]):
        wid = word_ids[i] if i < len(word_ids) else word_ids[0]
        r = s.post(f"{BASE}/review/sessions/{session_id}/answer/", json={
            "word_id": str(wid),
            "quality": quality,
            "response_time_ms": 2000 + i * 500
        })
        test(f"POST /review/sessions/{{id}}/answer/ (q={quality})", r)

# Complete
if session_id:
    r = s.post(f"{BASE}/review/sessions/{session_id}/complete/")
    test("POST /review/sessions/{id}/complete/", r)

r = s.get(f"{BASE}/review/history/")
test("GET /review/history/", r)

# ══════════════════════════════════════════════════
# D) TESTS
# ══════════════════════════════════════════════════
print("\n=== D) TESTS ===")
for tt in ["multiple_choice", "fill_blank", "context_guess", "mixed"]:
    r = s.post(f"{BASE}/tests/generate/", json={
        "test_type": tt,
        "question_count": 5,
        "difficulty": "adaptive"
    })
    test(f"POST /tests/generate/ ({tt})", r, [200, 201])
    if r.status_code in [200, 201]:
        td = r.json().get("data", r.json())
        # Session is nested:
        session_obj = td.get("session", {}) if isinstance(td, dict) else {}
        test_id = session_obj.get("id") or td.get("id") or td.get("session_id")
        questions = td.get("questions", [])
        print(f"  Test {tt}: {test_id}, questions: {len(questions)}")

        # Answer first question
        if questions and test_id:
            q = questions[0]
            qid = q.get("id")
            opts = q.get("options", ["test"])
            answer = opts[0] if opts else "test"
            r = s.post(f"{BASE}/tests/{test_id}/answer/", json={
                "question_id": str(qid),
                "answer": str(answer),
                "response_time_ms": 3000
            })
            test(f"POST /tests/{{id}}/answer/ ({tt})", r)

        # Complete
        if test_id:
            r = s.post(f"{BASE}/tests/{test_id}/complete/")
            test(f"POST /tests/{{id}}/complete/ ({tt})", r)

r = s.get(f"{BASE}/tests/history/")
test("GET /tests/history/", r)

# ══════════════════════════════════════════════════
# E) GAMES
# ══════════════════════════════════════════════════
print("\n=== E) GAMES ===")

# Speed round
r = s.post(f"{BASE}/games/speed-round/start/")
test("POST /games/speed-round/start/", r, [200, 201])
speed_session = None
if r.status_code in [200, 201]:
    gd = r.json().get("data", r.json())
    speed_session = gd.get("session_id") or gd.get("id")
    game_words = gd.get("words", [])
    print(f"  Speed round: session={speed_session}, words={len(game_words)}")

if speed_session:
    answers = []
    gd = r.json().get("data", r.json())
    for i, gw in enumerate(gd.get("words", [])[:7]):
        wid = gw.get("word_id") or gw.get("id")
        opts = gw.get("options", [])
        sel = opts[0] if i < 5 and opts else (opts[1] if len(opts) > 1 else "wrong")
        answers.append({"word_id": str(wid), "selected_answer": sel})
    r = s.post(f"{BASE}/games/speed-round/submit/", json={
        "session_id": str(speed_session),
        "answers": answers
    })
    test("POST /games/speed-round/submit/", r)

# Word match
r = s.post(f"{BASE}/games/word-match/start/")
test("POST /games/word-match/start/", r, [200, 201])
match_session = None
if r.status_code in [200, 201]:
    gd = r.json().get("data", r.json())
    match_session = gd.get("session_id") or gd.get("id")
    print(f"  Word match: session={match_session}")

if match_session:
    gd_saved = r.json().get("data", r.json())
    match_words = gd_saved.get("words", [])
    match_translations = gd_saved.get("translations", [])
    match_pairs = []
    for i, mw in enumerate(match_words):
        wid = mw.get("word_id") or mw.get("id")
        # Try to match correct translation
        trans = match_translations[i] if i < len(match_translations) else ""
        match_pairs.append({"word_id": str(wid), "selected_translation": trans})
    r = s.post(f"{BASE}/games/word-match/submit/", json={
        "session_id": str(match_session),
        "pairs": match_pairs,
        "time_seconds": 45
    })
    test("POST /games/word-match/submit/", r)

# Word context
r = s.post(f"{BASE}/games/word-context/start/")
test("POST /games/word-context/start/", r, [200, 201])
context_session = None
if r.status_code in [200, 201]:
    gd = r.json().get("data", r.json())
    context_session = gd.get("session_id") or gd.get("id")
    print(f"  Word context: session={context_session}")

if context_session:
    gd = r.json().get("data", r.json())
    ctx_questions = gd.get("questions", gd.get("words", []))
    ctx_answers = []
    for cq in ctx_questions[:5]:
        wid = cq.get("word_id") or cq.get("id")
        opts = cq.get("options", [])
        ctx_answers.append({"word_id": str(wid), "selected_answer": opts[0] if opts else "test"})
    r = s.post(f"{BASE}/games/word-context/submit/", json={
        "session_id": str(context_session),
        "answers": ctx_answers
    })
    test("POST /games/word-context/submit/", r)

r = s.get(f"{BASE}/games/history/")
test("GET /games/history/", r)

r = s.get(f"{BASE}/games/stats/")
test("GET /games/stats/", r)

# ══════════════════════════════════════════════════
# F) CHAT
# ══════════════════════════════════════════════════
print("\n=== F) CHAT ===")
r = s.post(f"{BASE}/chat/start/", json={"topic": "travel"})
test("POST /chat/start/", r, [200, 201])
chat_session_id = None
if r.status_code in [200, 201]:
    cd = r.json().get("data", r.json())
    chat_session_id = cd.get("session_id") or cd.get("id")
    print(f"  Chat: session={chat_session_id}")

if chat_session_id:
    r = s.post(f"{BASE}/chat/sessions/{chat_session_id}/message/", json={
        "message": "I like to travel to mountains"
    })
    test("POST /chat/sessions/{id}/message/", r)

    r = s.post(f"{BASE}/chat/sessions/{chat_session_id}/end/")
    test("POST /chat/sessions/{id}/end/", r)

r = s.get(f"{BASE}/chat/history/")
test("GET /chat/history/", r)

if chat_session_id:
    r = s.get(f"{BASE}/chat/sessions/{chat_session_id}/")
    test("GET /chat/sessions/{id}/", r)

# ══════════════════════════════════════════════════
# G) IMPORT
# ══════════════════════════════════════════════════
print("\n=== G) IMPORT ===")
r = s.post(f"{BASE}/words/import/analyze/", json={
    "text": "The inevitable consequence of climate change is that many species will face extinction. Scientists have gathered overwhelming evidence that demonstrates the severe impact on biodiversity. Despite the tremendous efforts of conservationists, the obstacles remain daunting.",
    "max_words": 10
})
test("POST /words/import/analyze/", r)
if r.status_code in [200, 201]:
    print(f"  Analyze response: {json.dumps(r.json(), indent=2)[:300]}")

r = s.post(f"{BASE}/words/import/add/", json={
    "words": [
        {"original_word": "consequence", "translation": "oqibat", "difficulty_level": "medium"},
    ]
})
test("POST /words/import/add/", r, [200, 201])

# Clean up imported word
rr = s.get(f"{BASE}/words/?search=consequence")
if rr.status_code == 200:
    df = rr.json().get("data", rr.json())
    results = df if isinstance(df, list) else df.get("results", []) if isinstance(df, dict) else []
    for rw in results:
        if rw.get("original_word") == "consequence":
            s.delete(f"{BASE}/words/{rw['id']}/")

# ══════════════════════════════════════════════════
# H) ANALYTICS
# ══════════════════════════════════════════════════
print("\n=== H) ANALYTICS ===")
r = s.get(f"{BASE}/analytics/overview/")
test("GET /analytics/overview/", r)

r = s.get(f"{BASE}/analytics/weekly/")
test("GET /analytics/weekly/", r)

r = s.get(f"{BASE}/analytics/monthly/")
test("GET /analytics/monthly/", r)

r = s.get(f"{BASE}/analytics/difficult-words/")
test("GET /analytics/difficult-words/", r)

r = s.get(f"{BASE}/analytics/word-progress/")
test("GET /analytics/word-progress/", r)

r = s.get(f"{BASE}/analytics/calendar/?year=2026&month=2")
test("GET /analytics/calendar/", r)

# ══════════════════════════════════════════════════
# I) PROGRESS & BADGES
# ══════════════════════════════════════════════════
print("\n=== I) PROGRESS & BADGES ===")
r = s.get(f"{BASE}/users/progress/")
test("GET /users/progress/", r)

r = s.get(f"{BASE}/users/xp-history/")
test("GET /users/xp-history/", r)

r = s.get(f"{BASE}/users/badges/")
test("GET /users/badges/", r)

r = s.get(f"{BASE}/badges/")
test("GET /badges/", r)

# ══════════════════════════════════════════════════
# J) NOTIFICATIONS
# ══════════════════════════════════════════════════
print("\n=== J) NOTIFICATIONS ===")
r = s.get(f"{BASE}/notifications/")
test("GET /notifications/", r)

r = s.get(f"{BASE}/notifications/unread-count/")
test("GET /notifications/unread-count/", r)

r = s.post(f"{BASE}/notifications/read/", json={"all": True})
test("POST /notifications/read/ (all=true)", r)

# ══════════════════════════════════════════════════
# K) ENRICHMENT
# ══════════════════════════════════════════════════
print("\n=== K) ENRICHMENT ===")
if word_id:
    r = s.post(f"{BASE}/words/{word_id}/enrich/")
    test("POST /words/{id}/enrich/", r, [200, 201, 202])

    r = s.get(f"{BASE}/words/{word_id}/enrichment-status/")
    test("GET /words/{id}/enrichment-status/", r)

r = s.post(f"{BASE}/words/enrich-all/")
test("POST /words/enrich-all/", r, [200, 201, 202])

# ══════════════════════════════════════════════════
# L) CONFUSING PAIRS
# ══════════════════════════════════════════════════
print("\n=== L) CONFUSING PAIRS ===")
r = s.get(f"{BASE}/words/confusing-pairs/")
test("GET /words/confusing-pairs/", r)

if r.status_code == 200:
    pairs = r.json().get("data", r.json())
    if isinstance(pairs, dict):
        pairs = pairs.get("results", [])
    if pairs:
        pair_id = pairs[0].get("id")
        r = s.get(f"{BASE}/words/confusing-pairs/{pair_id}/")
        test("GET /words/confusing-pairs/{id}/", r)

        r = s.post(f"{BASE}/words/confusing-pairs/{pair_id}/drill/")
        test("POST /words/confusing-pairs/{id}/drill/", r)

        r = s.get(f"{BASE}/words/confusing-pairs/count/")
        test("GET /words/confusing-pairs/count/", r)

# ══════════════════════════════════════════════════
# M) DAILY CHALLENGES
# ══════════════════════════════════════════════════
print("\n=== M) DAILY CHALLENGES ===")
r = s.get(f"{BASE}/challenges/today/")
test("GET /challenges/today/", r)

r = s.post(f"{BASE}/challenges/claim/")
test("POST /challenges/claim/", r, [200, 201, 400])

# ══════════════════════════════════════════════════
# SUMMARY
# ══════════════════════════════════════════════════
print("\n" + "=" * 60)
print(f"RESULTS: {len(successes)} passed, {len(errors)} failed")
print("=" * 60)
if errors:
    print("\nFAILED TESTS:")
    for e in errors:
        print(f"  ✗ {e}")
print()
