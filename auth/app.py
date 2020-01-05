from flask import Flask
from flask import request
from flask import make_response,render_template
import redis
app = Flask(__name__)
from .test import password_encryption,check_password
db = redis.Redis(host='client_redis', port=6381, decode_responses=True)

test=password_encryption("admin")
db.set("users:"+"admin",test)


@app.route('/')
def index():
    return render_template('login.html',WEB_HOST="/auth")

@app.route('/welcome')
def welcome():
  return "hello pIDR"

@app.route('/auth', methods=['POST'])
def auth():
  login = request.form.get('login')
  password = request.form.get('password')
  passwordDB=db.get("users:" + login)
  if check_password(passwordDB,password):
    response = make_response('', 303)
    response.headers["Location"] = "/file_manage"
    return response

@app.route('/file_manage',methods=['GET'])
def upload():
    return render_template("file_manage.html")

