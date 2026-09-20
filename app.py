from flask import Flask, render_template, request, redirect, url_for
from markupsafe import escape

app = Flask(__name__)

LESSONS = [
    {
        "title": "Input validation",
        "idea": "Treat browser input as untrusted data. Validate type, length, and allowed values on the server.",
        "task": "Find the validation rules in /profile and explain why they reduce unexpected input.",
    },
    {
        "title": "Output encoding",
        "idea": "When displaying user-controlled text, encode it for the context where it is inserted.",
        "task": "Submit a nickname containing HTML characters and observe that the page displays the text rather than executing it.",
    },
    {
        "title": "Authentication basics",
        "idea": "Authentication should use strong password hashing, secure sessions, rate limits, and careful error handling.",
        "task": "Read the login code and identify the security controls that should exist in a production application.",
    },
    {
        "title": "Security headers",
        "idea": "Headers such as Content-Security-Policy and X-Content-Type-Options add browser-side defenses.",
        "task": "Inspect the response headers and identify which defensive headers are present.",
    },
]

@app.after_request
def security_headers(response):
    response.headers["Content-Security-Policy"] = "default-src 'self'; style-src 'self' 'unsafe-inline'"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Referrer-Policy"] = "no-referrer"
    return response

@app.get("/")
def index():
    return render_template("index.html", lessons=LESSONS)

@app.route("/profile", methods=["GET", "POST"])
def profile():
    nickname = ""
    message = None
    if request.method == "POST":
        raw = request.form.get("nickname", "")
        # Defensive validation: limit length and reject control characters.
        if len(raw) > 30:
            message = "Nickname is too long."
        elif any(ord(ch) < 32 for ch in raw):
            message = "Nickname contains unsupported control characters."
        else:
            nickname = raw
            message = "Accepted safely. Flask/Jinja escapes it when rendering."
    return render_template("profile.html", nickname=nickname, message=message)

@app.get("/login")
def login():
    return render_template("login.html")

@app.post("/login")
def login_post():
    # This lab intentionally does not authenticate real accounts.
    # Never store plaintext passwords in a real application.
    username = request.form.get("username", "")
    return render_template(
        "login.html",
        message=f"Demo only: no account was authenticated for {escape(username)}."
    )

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
