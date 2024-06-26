from flask import (Flask, json, render_template, jsonify, request, redirect, session, url_for)
from flask_cors import CORS 
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta
from werkzeug.utils import secure_filename
from bson import ObjectId
import jwt
import hashlib
from pymongo import MongoClient
import bcrypt


app = Flask(__name__)

CORS(app)

# Load .env file
load_dotenv()

# Read environment variables
connection_string = os.getenv("DB_CONNECTION_STRING")
db_name = os.getenv("DB_NAME")
SECRET_KEY = os.getenv("SECRET_KEY")

# Set up MongoDB connection
client = MongoClient(connection_string)
db = client[db_name]

app.secret_key = SECRET_KEY

@app.route('/', methods=['GET'])
def home():
    token_receive = request.cookies.get("mytoken")
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=["HS256"])
        logged_in = db.user.find_one({"username": payload["id"]})
        return render_template('home.html', logged_in=logged_in)    
    except (jwt.ExpiredSignatureError,jwt.exceptions.DecodeError):
        return render_template('home.html')       

@app.route('/register')
def register():
    return render_template('register.html')

@app.route("/sign_up/save", methods=["POST"])
def sign_up():
    if request.method == "POST":
        username_receive = request.form['username_give']
        password_receive = request.form['password_give']
        password_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()

        doc = {
            "username": username_receive,
            "password": password_hash,  # Simpan password sebagai teks biasa (harap diperhatikan untuk keamanan)
            "profile_name": username_receive,
            "role": "player",
            "profile_pic": "",
            "profile_pic_default": "profile/Snorlaxv.png",
            "profile_info": ""
        }

        db.user.insert_one(doc)

        # Redirect ke halaman login setelah berhasil sign-up
        return redirect(url_for("login"))  # "login" adalah nama fungsi atau endpoint untuk halaman login
    
    return jsonify({'result': 'fail', 'msg': 'Invalid request'})

@app.route("/login")
def login():
    msg = request.args.get("msg")
    return render_template("login.html", msg=msg)

@app.route("/sign_in", methods=["POST"])
def sign_in():
    username_receive = request.form["username"]
    password_receive = request.form["password"]
    pw_hash = hashlib.sha256(password_receive.encode("utf-8")).hexdigest()

    result = db.user.find_one({"username": username_receive, "password": pw_hash})
    
    if result:
        # Generate JWT token
        payload = {"id": username_receive, "exp": datetime.utcnow() + timedelta(seconds=60 * 60 * 24)}
        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
        
        # Set token as cookie
        response = redirect(url_for("home"))
        response.set_cookie('mytoken', token, httponly=True, samesite='Strict')

        return response

    return jsonify({"result": "fail", "msg": "We could not find a user with that id/password combination"})

@app.route('/logout')
def logout():
    # Hapus cookie JWT ('mytoken')
    response = redirect(url_for('home'))  # Redirect ke halaman home setelah logout
    response.set_cookie('mytoken', '', expires=0, httponly=True, samesite='Strict')  # Hapus cookie 'mytoken' dengan mengeset expires=0

    return response

@app.route('/news')
def news():
    token_receive = request.cookies.get("mytoken")
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=["HS256"])
        logged_in = db.user.find_one({"username": payload["id"]})
        return render_template('news.html', logged_in=logged_in)    
    except (jwt.ExpiredSignatureError,jwt.exceptions.DecodeError):
        return render_template('news.html')

@app.route('/vokemon')
def vokemon():
    token_receive = request.cookies.get("mytoken")
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=["HS256"])
        logged_in = db.user.find_one({"username": payload["id"]})
        return render_template('vokemon.html', logged_in=logged_in)    
    except (jwt.ExpiredSignatureError,jwt.exceptions.DecodeError):
        return render_template('vokemon.html')

@app.route('/tournament')
def tournament():
    token_receive = request.cookies.get("mytoken")
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=["HS256"])
        logged_in = db.user.find_one({"username": payload["id"]})
        return render_template('tournament.html', logged_in=logged_in)    
    except (jwt.ExpiredSignatureError,jwt.exceptions.DecodeError):
        return render_template('tournament.html')

@app.route('/profile')
def profile():
    token_receive = request.cookies.get("mytoken")
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=["HS256"])
        logged_in = db.user.find_one({"username": payload["id"]})
        return render_template('profile.html', logged_in=logged_in)    
    except (jwt.ExpiredSignatureError,jwt.exceptions.DecodeError):
        return render_template('profile.html')

@app.route('/testing')
def testing():
    return render_template('testing.html')

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)