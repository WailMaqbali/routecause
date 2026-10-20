from engine import infer

def rule(id, cond, then, w=0.5):
    return {"id": id, "if": cond, "then": then, "weight": w, "why": "test"}

def test_rule_fires():
    r = infer({"a": "x"}, [rule("R1", {"a": "x"}, {"diagnosis": "D"}, 0.6)])
    assert r["ranked"] == [("D", 0.6)]

def test_rule_does_not_fire():
    r = infer({"a": "y"}, [rule("R1", {"a": "x"}, {"diagnosis": "D"})])
    assert r["ranked"] == [] and r["trace"] == []

def test_chaining():  # R1 derives a fact that R2 needs, even though R2 is listed first
    rules = [rule("R2", {"b": "1"}, {"diagnosis": "D"}),
             rule("R1", {"a": "x"}, {"fact": {"b": "1"}})]
    assert infer({"a": "x"}, rules)["ranked"][0][0] == "D"

def test_confidence_combines():
    rules = [rule("R1", {"a": "x"}, {"diagnosis": "D"}, 0.5),
             rule("R2", {"a": "x"}, {"diagnosis": "D"}, 0.5)]
    assert abs(infer({"a": "x"}, rules)["ranked"][0][1] - 0.75) < 1e-9

def test_list_condition():
    r = infer({"a": "y"}, [rule("R1", {"a": ["x", "y"]}, {"diagnosis": "D"})])
    assert r["ranked"]

def test_empty_input():
    assert infer({}, [])["ranked"] == []