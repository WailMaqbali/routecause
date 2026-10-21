import db

def test_rules_load_and_log(tmp_path):
    conn = db.init(str(tmp_path / "t.db"))          # temp DB, doesn't touch the real one
    assert len(db.get_rules(conn)) > 0
    db.log_consultation(conn, {"scope": "one"}, "X", 0.5)
    assert conn.execute("SELECT COUNT(*) FROM log").fetchone()[0] == 1