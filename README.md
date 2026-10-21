# RouteCause

A rule-based expert system that diagnoses common home Wi-Fi and home-network faults from things a non-technical user can actually observe (router light colours, which devices are affected, when it happens, what changed) and **explains why** it reached its conclusion.

Built for ICT206 Intelligent Systems, Murdoch University.

<!-- TODO: add a screenshot of the result page: docs/screenshot.png, then uncomment -->
<!-- ![RouteCause result page](docs/screenshot.png) -->

## The problem

Home users with no networking background hit problems like "my Wi-Fi keeps dropping" or "everything is slow in the evening". Their usual options are generic forum threads that may not match their symptoms, or an ISP chatbot that follows a fixed script and never explains itself. RouteCause targets a narrow domain: the most common causes of home Wi-Fi/network problems (not ISP infrastructure faults, not enterprise networking), diagnosed from evidence a user can observe, with every conclusion traceable to the rules that produced it.

## How it works

- **Knowledge base** (`rules.json`, loaded into SQLite): 35 IF-THEN rules, each with a hand-assigned confidence weight and a plain-English reason.
- **Inference engine** (`engine.py`): forward chaining. It starts from the user's answers and fires rules until none apply. Some rules derive *intermediate facts* (for example `network_wide`, `wifi_only`, `wired_also`) that later rules use, so the chaining is real and not a single lookup.
- **Confidence**: when several rules support the same diagnosis their weights combine with the MYCIN-style certainty-factor formula `cf = a + b * (1 - a)`, so scores stay between 0 and 1.
- **Explanation trace**: every rule that fired is recorded with the conditions it matched and its reason. The trace is shown on the results page.
- **Separation**: `engine.py` imports neither Flask nor SQLite. Rules can be edited without touching engine code.

The 10 multiple-choice questions cover: devices affected, wired vs Wi-Fi, symptom, recent change, power light, WAN light, timing, signal and distance, devices in use, and speed test result. The system distinguishes 12 diagnoses plus a low-confidence "Undetermined" fallback.

## Run it

```bash
git clone https://github.com/WailMaqbali/routecause.git
cd routecause
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

python app.py          # web app at http://127.0.0.1:5000
python evaluate.py     # accuracy on the labelled scenarios
python -m pytest -v    # unit and integration tests
```

## Evaluation

**Goals** (from the project proposal):
1. Primary: the top-ranked diagnosis matches the true diagnosis in at least 80% of labelled scenarios (at least 20 scenarios).
2. Secondary: every consultation produces a non-empty explanation trace.

**Method**: every scenario in `scenarios.json` is run through the real inference engine (`evaluate.py` and a pytest integration test). Accuracy is correct / total, and a trace is checked for each case. `tests/test_scenarios.py` fails if either goal is missed.

**Test set (33 scenarios)**
- **27 "tune" scenarios (S01-S27)**: written around common real-world patterns from home-networking forums (for example the NetSpot, EE, Netgear and SevenForums communities). These were drafted with Claude *after* the rules existed, so they are likely to flatter the rules. Treat the tune score as optimistic.
- **6 "holdout" scenarios (H01-H06)**: real forum threads where the original poster confirmed the fix, used only for evaluation and not for rule tuning. Where a thread did not state an answer, a neutral default was used (lights green, signal strong and near, load low, speed test not run). Each scenario lists exactly which answers were defaulted in its `assumed` field, and its source in `url`.

| ID | Real thread (confirmed fix) | True diagnosis |
|---|---|---|
| H01 | [Netgear R7450, specific sites not loading](https://community.netgear.com/discussions/home-wifi-routers-nighthawk/specific-sites-not-loading-with-r7450/2361205/replies/2361276) | DNS failure |
| H02 | [Netgear, Windows PC can't get an address over DHCP](https://community.netgear.com/discussions/Orbi/windows-pc-cant-connect-to-wifi-with-dhcp/1640064) | DHCP/IP conflict |
| H03 | [VideoHelp, slow internet only through router](https://forum.videohelp.com/threads/368305-[Solved]-Slow-internet-only-through-router) | Plan/speed mismatch |
| H04 | [EE community, router dropping every ~20 min](https://community.ee.co.uk/t5/Broadband-Landline/Router-issues-keeps-dropping-connection/m-p/1572759/highlight/true) | Router power/hardware fault |
| H05 | [Netgear R8000, daily drops after firmware update](https://community.netgear.com/discussions/home-wifi-routers-nighthawk/issue-with-r8000-firmware-v1-0-4-18-10-1-49/1592838/replies/1593489) | Faulty firmware update |
| H06 | [Netgear RAX120, unstable after firmware update](https://community.netgear.com/t5/Nighthawk-Routers-with-WiFi-6-AX/New-RAX120-Firmware-1-0-1-136-is-trash-I-rolled-back/m-p/1984234) | Faulty firmware update |

**Results**

| | Tune | Holdout | Overall | Empty traces |
|---|---|---|---|---|
| Untuned baseline (commit `3b44e01`) | 24/27 = 89% | 5/6 = 83% | 29/33 = 88% | 0 |
| After one rule refinement | 25/27 = 93% | 5/6 = 83% | 30/33 = 91% | 0 |

Both goals are met. The holdout set is only 6 cases, so read "5 of 6" as an indication, not a precise percentage.

## Error analysis

The baseline had four misses. I refined the rules only where the change was justified by networking logic, not by the test.

**Fixed: S08 (router needs a restart).** A low speed test on a wired connection triggered "Plan/speed mismatch" (72%) over "Router needs restart" (50%). A plan shortfall is constant, while a hung router slows down intermittently, so rule `R90` now requires `timing = always`. Two unit tests pin this behaviour (`tests/test_rules.py`).

**Tried and rejected.** Counting medium device load towards bandwidth saturation, to fix S26, did not fix S26 and broke S17 (accuracy fell back to 88%). The two scenarios have the same answers on the relevant questions, so no rule change separates them.

**Remaining misses (limits of the 10-question set, not rule bugs):**

| Case | What happened | What would fix it |
|---|---|---|
| S19 | One speaker drops when the microwave runs. The system says device adapter fault. | A question such as "does it drop when a microwave or cordless phone is on?" |
| S26 | Four people streaming at medium load. The system says channel congestion. | A finer-grained load question, or a "does it also happen outside the evening?" question |
| H04 | A failing power adapter with normal-looking lights. The system says 2.4GHz interference. | A question such as "did restarting the router fix it, even briefly?" |

A correct answer can also be fragile: for H05 (real firmware thread) the right diagnosis wins with 70% against 64% for 2.4GHz interference. The margin is thin.

## Limitations

- The scenarios were chosen by me (and drafted with AI), and the rules were designed by me. Even with real-thread holdout cases, the test set is a proxy for real-world performance and may fit the rules too neatly.
- The holdout set has only 6 cases and covers 5 of the 12 diagnoses. Most unstated answers in those threads were defaulted.
- Confidence weights are hand-assigned, not learned. They rank diagnoses sensibly but are not calibrated probabilities.
- The ideal evaluation would recruit real users with live problems and measure diagnostic outcome and time-to-resolution against a control group.

## Example traces

**S01: laptop with no internet after a new smart TV was added** (one device, connects but no internet, new device added, lights normal)

```
Likely cause: DHCP/IP conflict (76%), then Undetermined (10%)
R01  Only one device is affected, so the fault is likely local to it
R30  A new device joined and this one connects with no internet, which fits a duplicate IP
R31  One device with no internet can be an address lease problem
R99  Fallback: generic advice applies when nothing else matches strongly
Fix: restart the affected device to get a fresh address, or reserve it a fixed IP in the router settings.
```

**H05: real Netgear thread, daily drops after a firmware update** (correct, but a close call)

```
Likely cause: Faulty firmware update (70%), then 2.4GHz interference (64%)
R02  Most devices are affected, so the fault is likely in the network
R03  Wired devices are fine or absent, so the fault is likely in the Wi-Fi layer
R20  Network-wide problems began right after a firmware update
R21  This symptom started right after a firmware update
R63  Random Wi-Fi drop-outs near the router fit interference from microwaves, cordless phones or Bluetooth
R64  Random Wi-Fi-only drop-outs
R99  Fallback: generic advice applies when nothing else matches strongly
```

**H04: real EE thread, fixed by a replacement power adapter** (a miss, shown for transparency)

```
Top answer: 2.4GHz interference (64%). True cause: faulty power adapter.
R02  Most devices are affected, so the fault is likely in the network
R03  Wired devices are fine or absent, so the fault is likely in the Wi-Fi layer
R63  Random Wi-Fi drop-outs near the router fit interference from microwaves, cordless phones or Bluetooth
R64  Random Wi-Fi-only drop-outs
R99  Fallback: generic advice applies when nothing else matches strongly
```

The trace makes the failure easy to diagnose: no rule can see a failing adapter when the power light looks normal.

## Project structure

```
engine.py        forward-chaining inference engine (no Flask or SQLite imports)
rules.json       knowledge base (35 rules)
questions.py     the 10 questions and allowed answers
fixes.py         plain-English cause and fix for each diagnosis
db.py            SQLite: loads rules, logs each consultation
app.py           Flask web interface
templates/       questionnaire and result pages
scenarios.json   33 labelled test scenarios (27 tune, 6 holdout)
evaluate.py      accuracy harness
tests/           unit, integration and scenario tests
```

## Use of AI

Claude (Anthropic) was used to brainstorm project ideas, suggest the tech stack and architecture, format references, draft the rule base and the 27 tune scenarios, and search for and summarise the forum threads used as holdout cases. I reviewed the rules and scenarios, and the evaluation numbers above come from running the code in this repository.
