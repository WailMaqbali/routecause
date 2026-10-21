import json
from evaluate import run
from questions import QUESTIONS
from fixes import FIXES

def test_goals():
    stats, empty = run(verbose=False)
    h = sum(v[0] for v in stats.values()); t = sum(v[1] for v in stats.values())
    assert t >= 20            # enough scenarios
    assert h / t >= 0.80      # primary goal
    assert empty == 0         # secondary goal

def test_scenarios_are_valid():
    errors, seen = [], set()
    with open("scenarios.json") as f:
        for s in json.load(f):
            if s["id"] in seen: errors.append(f"{s['id']}: duplicate id")
            seen.add(s["id"])
            if s["true"] not in FIXES or s["true"] == "Undetermined":
                errors.append(f"{s['id']}: bad label '{s['true']}'")
            if s.get("set") not in ("tune", "holdout"):
                errors.append(f"{s['id']}: set must be tune or holdout")
            for k in QUESTIONS:           # every question must be answered
                if k not in s["answers"]: errors.append(f"{s['id']}: missing '{k}'")
            for k, v in s["answers"].items():   # every answer must be a real option
                if k not in QUESTIONS: errors.append(f"{s['id']}: unknown question '{k}'")
                elif v not in QUESTIONS[k][1]: errors.append(f"{s['id']}: '{v}' invalid for '{k}'")
    assert not errors, "\n".join(errors)