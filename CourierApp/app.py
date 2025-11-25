from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, User
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
import os

app = Flask(__name__)

# loading variables from .env file
load_dotenv() 

db=os.getenv("DATABASE")
postgres_passw=os.getenv("POSTGRES_PASSWORD")
postgres_user=os.getenv("POSTGRES_USER")

DATABASE_URL = f"postgresql+psycopg2://{postgres_user}:{postgres_passw}@localhost:5432/{db}"
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)  # Tworzymy tabele jeśli nie istnieją
Session = sessionmaker(bind=engine)

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    session = Session()
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        if session.query(User).filter_by(email=email).first():
            return render_template("register.html", error="Użytkownik już istnieje")

        hashed_password = generate_password_hash(password)
        new_user = User(email=email, password=hashed_password)
        session.add(new_user)
        session.commit()
        
        session.close()
        return redirect(url_for("authorized"))

    session.close()
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    session = Session()
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = session.query(User).filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            session.close()
            return redirect(url_for("authorized"))
        else:
            session.close()
            return render_template("login.html", error="Nieprawidłowy email lub hasło")

    session.close()
    return render_template("login.html")

@app.route("/authorized", methods=["GET"])
def authorized():
    return render_template("authorized.html")

if __name__ == "__main__":
    app.run(debug=True)
