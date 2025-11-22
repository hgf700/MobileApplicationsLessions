from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        if email == "123" and password == "123":
            return redirect(url_for("authorized"))

        return render_template("login.html", error="Nieprawidłowy login")

    return render_template("login.html")

@app.route("/register", methods=["GET"])
def register():
    return render_template("register.html")

@app.route("/authorized", methods=["GET"])
def authorized():
    return render_template("authorized.html")


if __name__ == "__main__":
    app.run(debug=True)
