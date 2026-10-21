from engine import infer, load_rules

RULES = load_rules()
BASE = {"scope": "most", "wired": "yes", "symptom": "slow", "change": "nothing", "power": "green",
        "wan": "green", "timing": "always", "signal": "strong_near", "load": "low", "speedtest": "low"}

def top(**override):
    return infer({**BASE, **override}, RULES)["ranked"][0][0]

def test_constant_shortfall_is_plan_mismatch():
    assert top() == "Plan/speed mismatch"

def test_intermittent_slowdown_is_not_plan_mismatch():  # plan shortfalls are constant, not random
    assert top(timing="random") != "Plan/speed mismatch"