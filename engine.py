import json

def load_rules(path="rules.json"):
    with open(path) as f:
        return json.load(f)

def combine(a, b):
    # MYCIN-style certainty factor combination, stays within 0..1
    return a + b * (1 - a)

def infer(answers, rules):
    facts = dict(answers)          # working memory
    fired, scores, trace = set(), {}, []
    changed = True
    while changed:                 # forward chain until no new rule fires
        changed = False
        for r in rules:
            if r["id"] in fired:
                continue
            # condition value may be a single value or a list of allowed values
            ok = all(facts.get(k) in (v if isinstance(v, list) else [v])
                     for k, v in r["if"].items())
            if not ok:
                continue
            fired.add(r["id"]); changed = True
            then = r["then"]
            if "fact" in then:
                facts.update(then["fact"])       # intermediate fact, may trigger more rules
            if "diagnosis" in then:
                d = then["diagnosis"]
                scores[d] = combine(scores.get(d, 0), r["weight"])
            trace.append({"rule": r["id"], "matched": r["if"], "why": r["why"]})
    ranked = sorted(scores.items(), key=lambda x: -x[1])
    return {"ranked": ranked, "trace": trace, "facts": facts}