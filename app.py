from flask import Flask, render_template, request, redirect, url_for, session
import json
from file import get_ai_msg

app = Flask(__name__)
app.secret_key = "cf8bcd5b6dcf3dd2beaa1534ad1720342e86ccb83f89913e17fd5df73bf0a02e"

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        patient_prompt = request.form.get("patient_prompt")
        ai_msg_json = get_ai_msg(patient_prompt)
        session["ai_msg_json"] = json.loads(ai_msg_json)  # Store AI data in session
        return redirect(url_for("medicine"))
    return render_template("index.html")

@app.route("/medicine")
def medicine():
    ai_msg_json = session.get("ai_msg_json", {})
    medicines = ai_msg_json.get("pharmacy", {}).get("medications", [])
    return render_template("medicine.html", medicines=medicines)

@app.route("/services")
def services():
    ai_msg_json = session.get("ai_msg_json", {})
    services = ai_msg_json.get("services", {}).get("tests", [])
    return render_template("services.html", services=services)

@app.route("/diagnosis")
def diagnosis():
    ai_msg_json = session.get("ai_msg_json", {})
    diagnosis = ai_msg_json.get("diagnosis", [])
    if isinstance(diagnosis, dict):
        diagnosis = [diagnosis]
    
    return render_template("diagnosis.html", diagnosis=diagnosis)

@app.route("/summary")
def summary():
    ai_msg_json = session.get("ai_msg_json", {})
    return render_template("summary.html", ai_msg_json=ai_msg_json)



if __name__ == "__main__":
    app.run(debug=True)

