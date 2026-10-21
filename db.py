import sqlite3, json

def init(db_path="routecause.db", rules_path="rules.json"):
    conn = sqlite3.connect(db_path, check_same_thread=False)  # Flask uses threads
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS rules(id TEXT PRIMARY KEY, body TEXT);
        CREATE TABLE IF NOT EXISTS log(
            id INTEGER PRIMARY KEY, ts TEXT DEFAULT CURRENT_TIMESTAMP,
            answers TEXT, diagnosis TEXT, confidence REAL);""")
    # re-seed rules from JSON on every start, so editing rules.json is enough
    conn.execute("DELETE FROM rules")
    with open(rules_path) as f:
        for r in json.load(f):
            conn.execute("INSERT INTO rules VALUES(?,?)", (r["id"], json.dumps(r)))
    conn.commit()
    return conn

def get_rules(conn):
    return [json.loads(b) for (b,) in conn.execute("SELECT body FROM rules ORDER BY id")]

def log_consultation(conn, answers, diagnosis, confidence):
    conn.execute("INSERT INTO log(answers, diagnosis, confidence) VALUES(?,?,?)",
                 (json.dumps(answers), diagnosis, confidence))
    conn.commit()