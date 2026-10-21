from flask import Flask, render_template, request
from engine import infer
from questions import QUESTIONS
from fixes import FIXES, DEFAULT
import db

app = Flask(__name__)
conn = db.init()

@app.route("/")
def index():
    return render_template("index.html", questions=QUESTIONS)

@app.route("/diagnose", methods=["POST"])
def diagnose():
    # keep only answered questions, so a skipped one doesn't crash
    answers = {k: request.form[k] for k in QUESTIONS if k in request.form}
    result = infer(answers, db.get_rules(conn))
    top, conf = result["ranked"][0] if result["ranked"] else ("Undetermined", 0.0)
    db.log_consultation(conn, answers, top, conf)
    cause, fix = FIXES.get(top, DEFAULT)
    return render_template("result.html", ranked=result["ranked"], trace=result["trace"],
                           cause=cause, fix=fix, top=top, fixes=FIXES)

if __name__ == "__main__":
    app.run(debug=True)