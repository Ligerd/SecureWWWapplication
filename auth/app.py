from flask import Flask
from flask import request
from flask import make_response,render_template
from uuid import uuid4
import redis
app = Flask(__name__)
from .chipter import encrypt,password_verification
db = redis.Redis(host='client_redis', port=6381, decode_responses=True)

test=encrypt("admin")
db.set("users:"+"admin",test)

SESSION_ID = "session-id"
SESSION_TIME = 180
INVALIDATE = -1

@app.route('/')
def index():
    return render_template('login.html',WEB_HOST="/auth")


@app.route('/auth', methods=['POST'])
def auth():
    login = request.form.get('login')
    password = request.form.get('password')
    passwordDB=db.get("users:" + login)
    response = make_response('', 303)
    if password_verification(passwordDB,password):
        session_id = str(uuid4())
        db.hset("session:" + session_id, "username", login)
        response.set_cookie(SESSION_ID, session_id, max_age=SESSION_TIME)
        response.headers["Location"] = "/file_manage"
        return response
    else:
        response.set_cookie(SESSION_ID, "INVALIDATE", max_age=INVALIDATE)
        response.headers["Location"] = "/error"
        return response

@app.route('/file_manage',methods=['GET'])
def upload():
    return render_template("file_manage.html",WEB_HOST="/auth")


@app.route('/logout')
def logout():
    response = make_response('', 303)
    response.set_cookie(SESSION_ID, "INVALIDATE", max_age=INVALIDATE)
    response.headers["Location"] = "/"
    return response

@app.route('/error',methods=['GET'])
def wrong():
    return render_template('error.html')