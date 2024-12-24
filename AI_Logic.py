import sys
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for session to work

@app.route("/", methods=["GET", "POST"])
def home():
    # Reset invalidcounter after successful navigation to 'about'
    if "invalidcounter" not in session:
        session["invalidcounter"] = 0

    if request.method == "POST":
        response = request.form.get("response", "").lower()

        if response == "nothing":
            return redirect(url_for("endloop"))
        elif response == "something":
            return redirect(url_for("somethingloop"))
        elif response == "everything":
            return redirect(url_for("everythingloop"))
        elif response == "about":
            return render_template("about.html")
        else:
            # Increment invalid counter and check if it exceeds limit
            session["invalidcounter"] += 1
            if session["invalidcounter"] >= 5:
                return redirect(url_for("endloop"))
            return render_template("index.html", message="Invalid input. Please enter 'nothing', 'something', 'everything', or 'about'.")

    return render_template("index.html")

@app.route("/endloop")
def endloop():
    # Reset session counters
    session.pop("invalidcounter", None)
    session.pop("looprun", None)
    return "<h1>Goodbye! Why are you so rude!</h1>"

@app.route("/somethingloop")
def somethingloop():
    # Use templates for better HTML management and flexibility
    return render_template("somethingloop.html")

@app.route("/everythingloop")
def everythingloop():
    looprun = session.get("looprun", 0)
    if looprun < 500:
        looprun += 5
        session["looprun"] = looprun
        return render_template("everythingloop.html", looprun=looprun)
    
    session["looprun"] = 0  # Reset the loop for the next session
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)
