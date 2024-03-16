from flask import Flask, jsonify, render_template, url_for, request, redirect
from pymongo import MongoClient
from Backend.database import loginAndRegisterDataBase
app = Flask(__name__, static_url_path='/static') 

@app.route("/", methods=["GET"])
def loginPage():
    return  render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    name = request.form['username']
    password = request.form['password']
        
    return redirect('/homePage')
@app.route('/homePage', methods=['GET', 'POST'])
def homePage():
    return render_template("homePage.html")

if __name__ == "__main__":
    # Please do not set debug=True in production
    app.run(host="0.0.0.0", port=5000, debug=True)