from flask import Flask
from flask import request
from flask import make_response, render_template, redirect
from uuid import uuid4
import redis
from jwt import encode,decode, InvalidTokenError
app = Flask(__name__)
from .chipter import encrypt,password_verification
from .service.user_service import UserService
from .request.user_request import UserRequest
from .service.note_service import NoteService
from .request.note_request import NoteRequest
import datetime

db = redis.Redis(host='client_redis', port=6381, decode_responses=True)

user_servise=UserService()
note_servise=NoteService()
test=encrypt("admin")
user_servise.addTestUser("admin",test)

SESSION_ID = "session-id"
SESSION_TIME = 180
INVALIDATE = -1
JWT_SECRET="HELLO"
JWT_SESSION_TIME=30
JWT_SECREATE_DATABASE="SECRET"

@app.route('/')
def index():
    return render_template('login.html')


@app.route('/auth', methods=['POST'])
def auth():
    user_req = UserRequest(request)
    response = make_response('', 303)
    user=user_servise.find_by_login(user_req.login)
    if user!=None:
        if password_verification(user.password,user_req.password):
            session_id = str(uuid4())
            db.hset("session:" + session_id, "username", user.login)
            response.set_cookie(SESSION_ID, session_id, max_age=SESSION_TIME)
            response.headers["Location"] = "/note_manage"
            return response
        else:
            response.set_cookie(SESSION_ID, "INVALIDATE", max_age=INVALIDATE)
            response.headers["Location"] = "/error"
            return response
    else:
        response.set_cookie(SESSION_ID, "INVALIDATE", max_age=INVALIDATE)
        response.headers["Location"] = "/error"
        return response

@app.route('/note_manage',methods=['GET','POST'])
def note_manage():
    session_id = request.cookies.get(SESSION_ID)
    if session_id:
        content_type="text/plain"
        login = db.hget("session:" + session_id, "username")
        allfids= db.hvals("notes:"+login)
        print(allfids)
        download_tokens=[]
        notes=[]
        for fidx in allfids:
            download_tokens.append(create_download_token(fidx).decode())
            notes.append(db.hget("shortcut:"+login,fidx))
        upload_token = create_upload_token().decode('ascii')
        return render_template("file_manage.html",allfids=allfids,content_type=content_type,upload_token=upload_token,download_tokens=download_tokens,filenames=notes)
    return my_redirect("/")

app.config["ALLOWED_FORMAT"]=["PDF"]



@app.route("/upload",methods=["POST"])
def upload_note():
    print(request.form.get('shortcut'))
    note_req = NoteRequest(request)
    t = request.form.get('token')
    c = request.form.get('callback')
    if t is None:
        return redirect(f"{c}?error=No+token+provided") if c \
            else ('<h1>CDN</h1> No tfilenamesoken provided', 401)
    if not valid(t):
        return redirect(f"{c}?error=Invalid+token") if c \
            else ('<h1>CDN</h1> Invalid token', 401)

    session_id = request.cookies.get(SESSION_ID)
    login=db.hget("session:" + session_id, "username")
    user=user_servise.find_by_login(login)
    fid, content_type = str(uuid4()),"text/plain"
    shortcat=note_servise.saveNote(note_req,user.id,fid)
    return redirect(f"{c}?fid={fid}&content_type={content_type}&shortcat={shortcat}") if c \
        else (f'<h1>CDN</h1> Uploaded {fid}', 200)

@app.route('/callback')
def uploaded():
    session_id = request.cookies.get(SESSION_ID)

    fid = request.args.get('fid')
    err = request.args.get('error')
    shortcat=request.args.get('shortcat')

    if not session_id:
        return my_redirect("/")
    if err:
        if err=="Invalid format file":
            return my_redirect("/format_error")
        return f"<h1>APP</h1> Upload failed: {err}", 400
    if not fid:
        return f"<h1>APP</h1> Upload successfull, but no fid returned", 500
    new_fied_prefix = str(db.incr(JWT_SECREATE_DATABASE))
    new_fied= new_fied_prefix + fid
    login = db.hget("session:"+session_id,"username")
    db.hset("notes:"+login,new_fied, fid)
    db.hset("shortcut:"+login,fid,shortcat)
    return my_redirect("/note_manage")


@app.route('/download/<fid>')
def download(fid):
    token = request.headers.get('token') or request.args.get('token')
    if len(fid) == 0:
        return '<h1>CDN</h1> Missing fid', 404
    if token is None:
        return '<h1>CDN</h1> No token', 401
    if not valid(token):
        return '<h1>CDN</h1> Invalid token', 401
    payload = decode(token, JWT_SECRET)
    if payload.get('fid', fid) != fid:
        return '<h1>CDN</h1> Incorrect token payload', 401
    note=note_servise.find_by_fid(fid)
    return render_template("note.html",shortcut=note.shortcut,note=note.note)

@app.route('/logout')
def logout():
    response = make_response('', 303)
    response.set_cookie(SESSION_ID, "INVALIDATE", max_age=INVALIDATE)
    response.headers["Location"] = "/"
    return response

@app.route('/error',methods=['GET'])
def wrong():
    return render_template('error.html')

def create_download_token(fid):
    exp = datetime.datetime.utcnow() + datetime.timedelta(seconds=JWT_SESSION_TIME)
    return encode({"iss":"CLIENT", "exp":exp}, JWT_SECRET, "HS256")

def create_upload_token():
    exp = datetime.datetime.utcnow() + datetime.timedelta(seconds=JWT_SESSION_TIME)
    return encode({"iss":"CLIENT", "exp":exp}, JWT_SECRET, "HS256")

def my_redirect(location):
    response = make_response('', 303)
    response.headers["Location"] = location
    return response

def valid(token):
    try:
       decode(token, JWT_SECRET)
    except InvalidTokenError as e:
       app.logger.error(str(e))
       return False
    return True