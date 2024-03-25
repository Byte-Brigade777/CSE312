from flask import Flask, jsonify, render_template, url_for, request, redirect, Response, make_response
from pymongo import MongoClient
from Backend.database import loginAndRegisterDataBase
from Backend.Login import LoginAndRegistration

app = Flask(__name__, static_url_path='/static') 
accountInfo = LoginAndRegistration(loginAndRegisterDataBase())

@app.after_request
def add_nosniff(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    return response

@app.route("/", methods=["GET"])
def loginPage():
    
    response = make_response(render_template('/index.html', error=accountInfo.errorMessage))
    accountInfo.errorMessage = ''
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['Contection'] = 'keep-alive'
    response.status_code = 200
    return response


@app.route('/login', methods=['POST'])
def login():
    name = request.form['username']
    password = request.form['password'] 
    info = accountInfo.login(name, password)
    if info[0]:
        response = make_response(render_template('/homePage.html'))
        response.set_cookie('token', info[1], httponly=True, max_age=3600)
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['Contection'] = 'keep-alive'
        return response
    return redirect('/')

@app.route("/Register", methods = ['GET', 'POST'])
def registerPage():
    
    response = make_response(render_template('registerPage.html', error=accountInfo.errorMessage))
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['Contection'] = 'keep-alive'
    response.status_code = 200
    accountInfo.errorMessage = ''
    return response


@app.route('/signup', methods=['POST'])
def signUp():
    name = request.form['newUsername']
    password = request.form['newPassword']
    confPassword = request.form['confirmPassword']
    if accountInfo.create_account(name, password, confPassword):
        return redirect('/')

    return redirect('/Register')

if __name__ == "__main__":
    # Please do not set debug=True in production
    app.run(host="0.0.0.0", port=8080, debug=True)