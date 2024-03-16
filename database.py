from pymongo import MongoClient
from flask import Flask, render_template, request, redirect, url_for, session, Response, flash, make_response, jsonify
import uuid
import bcrypt
import hashlib
import auth

app = Flask(__name__)

mongo_client = MongoClient("mongo")
db = mongo_client["cse312project"]
user_collection = db["users"]

@app.route("/register", methods =["POST"]) ##########Argument of type "() -> (Response | None)" cannot be assigned to parameter of type "T_route@route"
def register():
    msg = ""
    if request.method == "POST" and "newUsername" in request.form and "newPassword" in request.form and "confirmPassword" in request.form:
        user_data = request.get_json()
        username = user_data.get("newUsername")
        password = user_data.get("newPassword")
        password_confirm = user_data.get("confirmPassword")
        # check if two passwords match
        if (password != password_confirm):
            msg = "Passwords did not match"
            flash(msg)
            return redirect("/") ########### not sure yet if this works
        # check if user already exists
        if user_collection.find_one({"username":username}):
            msg = "User already exists"
            flash(msg)
            return redirect("/")
        valid = auth.validate_password(password)
        if valid == False:
            msg = "Password must be at least 8 characters with at least one of each of the following: Uppercase letter, lowercase letter, number, and one of these special characters: {'!', '@', '#', '$', '%', '^', '&', '(', ')', '-', '_', '='}"
            flash(msg)
            return redirect("/")
        bytes = password.encode('utf-8')
        salt = bcrypt.gensalt()
        hash = bcrypt.hashpw(bytes,salt)
        user_collection.insert_one({"username":username,"password":hash})
        resp = make_response(jsonify({'msg': 'User registered successfully'}), 201)
        resp.mimetype = "text/plain"
        resp.headers["X-Content-Type-Options"] = "nosniff"
        resp.headers["Location"] = '/'  ###################### is this going to be the actual home path
        return resp
        