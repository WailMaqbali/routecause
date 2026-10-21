import json
from engine import infer, load_rules

def run(path="scenarios.json", rules_path="rules.json", verbose=True):
    rules = load_rules(rules_path)
    stats, empty = {}, 0                 # split name -> [hits, total]
    with open(path) as f:
        scenarios = json.load(f)
    for s in scenarios:
        r = infer(s["answers"], rules)
        top = r["ranked"][0][0] if r["ranked"] else None
        empty += not r["trace"]          # secondary goal: trace must be non-empty
        st = stats.setdefault(s.get("set", "tune"), [0, 0])
        st[1] += 1
        if top == s["true"]:
            st[0] += 1
        elif verbose:
            print(f"MISS {s['id']}: got {top}, expected {s['true']}")
    return stats, empty

if __name__ == "__main__":
    stats, empty = run()
    for name, (h, t) in stats.items():
        print(f"{name}: {h}/{t} = {h/t:.0%}")
    h = sum(v[0] for v in stats.values()); t = sum(v[1] for v in stats.values())
    print(f"OVERALL: {h}/{t} = {h/t:.0%} | empty traces: {empty}")