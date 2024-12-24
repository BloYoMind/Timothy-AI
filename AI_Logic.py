import sys
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for session to work

# Global variables for state management (using session instead)
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        response = request.form.get("response", "").lower()

        if response == "nothing":
            return redirect(url_for("endloop"))
        elif response == "something":
            return redirect(url_for("somethingloop"))
        elif response == "everything":
            return redirect(url_for("everythingloop"))
        else:
            invalidcounter = session.get("invalidcounter", 0) + 1
            session["invalidcounter"] = invalidcounter
            if invalidcounter >= 5:
                return redirect(url_for("endloop"))
            return render_template("Timothy_AI.html", message="Invalid input. Please enter 'nothing', 'something', or 'everything'.")
    return render_template("Timothy_AI.html")

@app.route("/endloop")
def endloop():
    return "<h1>Goodbye! Why are you so rude!</h1>"

@app.route("/somethingloop")
def somethingloop():
    html_content = '<a href="https://www.esv.org/Genesis+1/">Click here to learn something.</a>'
    return f"<h1>Here is something about something:</h1><p>{html_content}</p>"

@app.route("/everythingloop")
def everythingloop():
    looprun = session.get("looprun", 0)
    if looprun < 500:
        looprun += 5
        session["looprun"] = looprun
        return f"""
        <h1>Everything</h1>
        <p>Wassup<br>everything<br>everything<br>everything<br>everything</p>
        <a href="{url_for('everythingloop')}">Continue Everything</a>
        """
    
    session["looprun"] = 0  # Reset the loop for the next session
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)
