from flask import Flask, render_template, url_for, session, redirect, request
from authlib.integrations.flask_client import OAuth
import firebase_admin
from firebase_admin import db, credentials
import os
import json

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY")
oauth = OAuth(app)
google = oauth.register(
    name="google",
    client_id=os.environ.get("CLIENT_ID"),
    client_secret=os.environ.get("CLIENT_SECRET"),
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs = {"scope":"openid profile email"}
)

cred = credentials.Certificate(json.loads(os.environ.get("FIREBASE_JSON")))
firebase_admin.initialize_app(cred, {
    "databaseURL": "https://calculus-world-cup-bb810-default-rtdb.europe-west1.firebasedatabase.app/"})
ref = db.reference()
user_ref = ref.child("users")

@app.route('/')
def unlogged():
    if "user" in session:
        return redirect(url_for("home"))
    return render_template('index.html')

@app.route("/login/google")
def login_google():
    try:
        redirect_uri = url_for("authorize_google",_external=True)
        return google.authorize_redirect(redirect_uri)
    except Exception as e:
        app.logger.error(f"Error during login: {str(e)}")
        return "Error during login", 500

@app.route("/authorize/google")
def authorize_google():
    token = google.authorize_access_token()
    userinfo_endpoint = google.server_metadata["userinfo_endpoint"]
    resp = google.get(userinfo_endpoint)
    user_info = resp.json()
    email = user_info["email"]
    fname = user_info["given_name"]
    lname = user_info["family_name"]
    uuid = user_info["sub"]
    session["user"] = uuid

    data = {"email": email,
           "first_name": fname,
           "last_name": lname}

    try:
        user_ref.child(uuid).set(data)
    except Exception as e:
        app.logger.error(f"Error with database: {str(e)}")
        return "Error with database", 500
        
    return redirect(url_for("home"))
    
@app.route("/home", methods=["GET","POST"])
def home():
    if request.method == "POST":
        group_a = request.form.get("group_a")
        group_b = request.form.get("group_b")
        group_c = request.form.get("group_c")
        group_d = request.form.get("group_d")
        group_e = request.form.get("group_e")
        if not(group_a and group_b and group_c and group_d and group_e):
            return render_template('main.html', name=user["first_name"]) #add error handling here
        else:
            #submit to database
            pass
    
    if "user" in session:
        uuid = session["user"]
    else:
        app.logger.error(f"Error: User not logged in")
        return redirect(url_for("unlogged"))

    
    user = user_ref.child(uuid).get()
    app.logger.info(f"session: {session}")
    
    if user:
        app.logger.info(f"User with uuid: {uuid}, info: {user}")
    else:
        app.logger.error(f"Error: User doesn't exist")
        return "User not found", 404
        
    return render_template('main.html', name=user["first_name"])
    
if __name__ == "__main__":
    app.run(debug=True)
