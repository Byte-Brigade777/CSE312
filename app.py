from flask import Flask, jsonify, render_template, url_for, request, redirect, Response, make_response, \
    send_from_directory, send_file
from pymongo import MongoClient
from Backend.database import loginAndRegisterDataBase, postContent
from Backend.Login import LoginAndRegistration
from Backend.postInformation import StoreInformation
import logging
import os
from werkzeug.utils import secure_filename

app = Flask(__name__, static_url_path='/static')
accountInfo = LoginAndRegistration(loginAndRegisterDataBase())
post_info = StoreInformation(postContent(), accountInfo)

# Specify the upload directory for when images are uploaded
UPLOAD_FOLDER = '/static/img'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.after_request
def add_nosniff(response):
    info = response.headers.get("Content-Disposition")
    mime_type = {'js': ['Content-Type', 'application/javascript'],
                 'css': ['Content-Type', 'text/css']}
    if info:
        for i in mime_type:

            if info.__contains__(i):
                app.logger.info(mime_type[i][0])
                app.logger.info(mime_type[i][1])

                response.headers[mime_type[i][0]] = mime_type[i][1]

    response.headers['X-Content-Type-Options'] = 'nosniff'
    return response


@app.route("/", methods=["GET"])
def login_page():
    if accountInfo.cookie_correct(request)[0] == True:
        app.logger.info('Triggered this conditation for some reason')
        return redirect('/Home')

    response = make_response(render_template('/index.html', error=accountInfo.errorMessage))
    accountInfo.errorMessage = ''
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.status_code = 200
    return response


@app.route('/login', methods=['POST'])
def home_page():
    name = request.form['username']
    password = request.form['password']
    info = accountInfo.login(name, password)

    if info[0]:
        return redirect('/Home')

    return redirect('/')


@app.route('/Home', methods=['GET', 'POST'])
def actual_home_page():
    logInformation = accountInfo.cookie_correct(request)
    app.logger.info(accountInfo.messageId)

    if accountInfo.count == 1:
        accountInfo.count = 0
        response = make_response(render_template('/homePage.html', Username=accountInfo.name))
        response.set_cookie('token', accountInfo.messageId, httponly=True, max_age=3600)
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['Connection'] = 'keep-alive'
        return response

    if logInformation[0] == True:
        response = make_response(render_template('/homePage.html', Username=accountInfo.name))
        response.set_cookie('token', accountInfo.messageId, httponly=True, max_age=3600)
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['Connection'] = 'keep-alive'
        return response

    return redirect('/')


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    if accountInfo.logout(request):
        response = make_response("Success Logout")
        response.status_code = 200
        return response
    response = make_response("Failed Logout")
    response.status_code = 404
    return response


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


@app.route('/add', methods=['POST', "GET"])
def addContent():
    post_info.storeRequest(request)
    response = make_response("Successfully added")
    response.status_code = 201
    return response


@app.route('/posts', methods=["POST", "GET"])
def send_post():
    listOfMessage = post_info.sendPost(request)
    return jsonify(listOfMessage)


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return jsonify({'message': 'No file part in the request'}), 400
        file = request.files['file']
        if file.filename == '':
            return jsonify({'message': 'No file selected'}), 400
        if file and allowed_file(file.filename):
            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            return jsonify({'message': 'File uploaded successfully', 'filename': filename}), 200
        return jsonify({'message': 'File type not allowed'}), 400
    elif request.method == 'GET':
        return render_template('upload.html')
def allowed_file(filename):
  ALLOWED_EXTENSIONS = {'jpg', 'jpeg'}
  return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# @app.route('/static/js/<path:filename>')
# def send_js(filename):
#     app.logger.info("It got called")
#     return send_file('static/js/' + filename)


# @app.route('/static/css/<path:filename>')
# def send_css(filename):
#     return send_file('static/css/' + filename, mimetype='text/css')


if __name__ == "__main__":
    # Please do not set debug=True in production
    app.run(host="0.0.0.0", port=8080, debug=True)
    app.logger.setLevel(logging.DEBUG)
