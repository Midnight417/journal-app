from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from datetime import date, datetime
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
import mysql.connector
import json
from helpers import login_required

mydb = mysql.connector.connect(
  host="localhost",
  user="someone",
  password="password",
  database="journaldatabase"
)

mycursor = mydb.cursor(dictionary=True)

app = Flask(__name__)


app.config["TEMPLATES_AUTO_RELOAD"] = True

@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route("/")
def index():
    return render_template("layout.html")


@app.route("/journal", methods=["GET","POST"])
@login_required
def journal():
    if request.method == "GET":
        sql = "SELECT section FROM journalentries WHERE user_id = %s GROUP BY section ORDER BY date DESC;"
        val = (session["user_id"],)
        mycursor.execute(sql, val)
        sections = mycursor.fetchall()
        for section in sections:
            section['data'] = datetime.strptime(section["section"], '%B %Y').date()
        
        sql = "SELECT * FROM journalentries WHERE user_id = %s ORDER BY date DESC;"
        val = (session["user_id"],)
        mycursor.execute(sql, val)
        entries = mycursor.fetchall()

        for entry in entries:
            entry['date'] = entry["date"].date().isoformat()

        return render_template("journal.html", sections=sections, entries=entries, length=len(entries))
    else:
        journal_id = request.form.get("journal-id")
        title = request.form.get("title")
        entry = request.form.get("entry")

        sql = "UPDATE journalentries SET title = %s, entry = %s WHERE id = %s;"
        val = (title, entry, journal_id)

        mycursor.execute(sql, val)
        
        mydb.commit()
        return redirect("/journal")

@app.route("/newjournalentry", methods=["POST"])
def newjournalentry():
    sql = "INSERT INTO journalentries (user_id, section, title, date, entry) VALUES (%s, %s, %s, %s, %s);"
    val = (session["user_id"], date.today().strftime("%B %Y"), "Untitled", datetime.now().isoformat(),"")
    mycursor.execute(sql, val)
    mydb.commit()
    return redirect("/journal")

@app.route("/deletejournalentry", methods=["POST"])
def deletejournalentry():

    deletion_id = request.form.get("deletion-id")

    sql = "DELETE FROM journalentries WHERE id = %s;"
    val = (deletion_id,)

    mycursor.execute(sql, val)
    mydb.commit()
    
    return redirect("/journal")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("/login.html")
    else:
        session.clear()

        if not request.form.get("username"):
            flash('You must provide a username!')
            return redirect("/login")
        elif not request.form.get("password"):
            flash('You must provide a password!')
            return redirect("/login")

        sql = "SELECT * FROM users WHERE username = %s;"
        val = (request.form.get("username"),)
        mycursor.execute(sql, val)
        rows = mycursor.fetchall()

        if rows:
            if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
                flash('Invalid username and/or password!')
                return redirect("/login")
            session["user_id"] = rows[0]["id"]

            return redirect("/journal")
            
        flash('Invalid username and/or password!')
        return redirect("/login")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    else:

        sql = "SELECT username FROM users WHERE username = %s;"
        val = (request.form.get("username"),)
        mycursor.execute(sql, val)
        exists = mycursor.fetchall()

        if not request.form.get("username"):
            flash('You must provide a username!')
            return redirect("/register")

        elif exists:
            flash('Username already exists!')
            return redirect("/register")

        elif not request.form.get("password"):
            flash('You must provide a password!')
            return redirect("/register")

        elif not request.form.get("passwordconfirm"):
            flash('You must confirm your password!')
            return redirect("/register")

        elif request.form.get("password") != request.form.get("passwordconfirm"):
            flash('Your passwords do not match!')
            return redirect("/register")

        sql = "INSERT INTO users (username, hash) VALUES (%s, %s);"
        val = (request.form.get("username"), generate_password_hash(request.form.get("password"),
                    method='pbkdf2:sha256', salt_length=8))
        mycursor.execute(sql, val)
        mydb.commit()

        sql = "SELECT * FROM users WHERE username = %s;"
        val = (request.form.get("username"),)
        mycursor.execute(sql, val)
        rows = mycursor.fetchall()

        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
                flash('Invalid username and/or password!')
                return redirect("/login")
        
        session["user_id"] = rows[0]["id"]

        return redirect("/journal")