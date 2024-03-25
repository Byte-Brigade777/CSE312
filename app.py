from flask import Flask, jsonify, render_template, url_for, request, redirect, Response, make_response
from pymongo import MongoClient
from Backend.database import loginAndRegisterDataBase
from Backend.Login import LoginAndRegistration
import logging

app = Flask(__name__, static_url_path='/static')
accountInfo = LoginAndRegistration(loginAndRegisterDataBase())

@app.after_request
def add_nosniff(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    return response

@app.route("/", methods=["GET"])
def login_page():
    
    app.logger.info(accountInfo.cookie_correct(request))
    if accountInfo.cookie_correct(request)[0] == True:
        app.logger.info('Triggered this conditation for some reason')

        return redirect('/Home')
    
    response = make_response(render_template('/index.html', error=accountInfo.errorMessage))
    accountInfo.errorMessage = ''
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['Connection'] = 'keep-alive'
    response.status_code = 200
    return response


@app.route('/Login', methods=['POST'])
def home_page():
    name = request.form['username']
    password = request.form['password']
    info = accountInfo.login(name, password)        

    if info[0]:
        return redirect('/Home')
    
    return redirect('/')

    
@app.route('/Home', methods=['GET','POST'])
def actual_home_page():
    logInformation = accountInfo.cookie_correct(request)
    app.logger.info(accountInfo.messageId)     
    
    if accountInfo.count == 1:
        accountInfo.count = 0
        response = make_response(render_template('/homePage.html', Username = accountInfo.name))
        response.set_cookie('token', accountInfo.messageId, httponly=True, max_age=3600)
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['Connection'] = 'keep-alive'
        return response
    
    if logInformation[0] == True: 
        app.logger.info(f'True is Triggered {logInformation[0]}')
        response = make_response(render_template('/homePage.html', Username = accountInfo.name))
        response.set_cookie('token', accountInfo.messageId, httponly=True, max_age=3600)
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['Connection'] = 'keep-alive'
        return response
    
    return redirect('/')
        

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    accountInfo.logout(request)
    return redirect('/')
    

@app.route("/Register", methods=['GET', 'POST'])
def register_page():
    response = make_response(render_template('registerPage.html', error=accountInfo.errorMessage))
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['Connection'] = 'keep-alive'
    response.status_code = 200
    accountInfo.errorMessage = ''
    return response

@app.route('/signup', methods=['POST'])
def sign_up():
    name = request.form['newUsername']
    password = request.form['newPassword']
    confPassword = request.form['confirmPassword']
    if accountInfo.create_account(name, password, confPassword):
        return redirect('/')

    return redirect('/Register')

if __name__ == "__main__":
    # Please do not set debug=True in production
    app.run(host="0.0.0.0", port=8080, debug=True)
    app.logger.setLevel(logging.DEBUG)
