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
    if "user" in session:        #user already logged in
        return redirect(url_for("vote"))
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
    pfp = user_info["picture"]
    session["user"] = uuid

    data = {"email": email,
           "first_name": fname,
           "last_name": lname,
           "pfp": pfp}

    user = user_ref.child(uuid).get()
    if user:         #user already exists
        return redirect(url_for("vote"))
    else:            #user doesn't exist
        try:
            user_ref.child(uuid).set(data)
        except Exception as e:
            app.logger.error(f"Error with database: {str(e)}")
            return "Error with database", 500
            
        return redirect(url_for("vote"))
    
@app.route("/vote", methods=["GET","POST"])
def vote():
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
        session.pop("user")
        return "User not found", 404

    gamble = user_ref.child(uuid).child("gamble").get()
    if gamble:    #already voted
        return redirect(url_for("profile"))
        
    if request.method == "POST":
        group_a = request.form.get("group_a")
        group_b = request.form.get("group_b")
        group_c = request.form.get("group_c")
        group_d = request.form.get("group_d")
        group_e = request.form.get("group_e")
        data = {"group_a_selection": group_a,
                "group_b_selection": group_b,
               "group_c_selection": group_c,
               "group_d_selection": group_d,
               "group_e_selection": group_e}
        try:
            user_ref.child(uuid).child("gamble").set(data)
        except Exception as e:
            app.logger.error(f"Error with database: {str(e)}")
            return "Error with database", 500
        return redirect(url_for("profile"))
    
    return render_template('vote.html', name=user["first_name"])

@app.route('/profile')
def profile():
    if "user" in session:
        uuid = session["user"]
    else:
        app.logger.error(f"Error: User not logged in")
        return redirect(url_for("unlogged"))

    user = user_ref.child(uuid).get()
    app.logger.info(f"session: {session}")
    if user:
        app.logger.info(f"User profile with uuid: {uuid}, info: {user}")
    else:    #user doesn;t exist
        app.logger.error(f"Error: User doesn't exist")
        session.pop("user")
        return "User not found", 404
    
    gamble = user_ref.child(uuid).child("gamble").get()
    if gamble:
        app.logger.info(f"User with uuid: {uuid}, gambling with: {gamble}")
    else:    #user hasn't voted yet
        app.logger.error(f"Error: User hasn't voted yet")
        return redirect(url_for("vote"))

    comp_ref = ref.child("competitors")
    selections = [gamble["group_a_selection"].title(), gamble["group_b_selection"].title(), gamble["group_c_selection"].title(), gamble["group_d_selection"].title(), gamble["group_e_selection"].title()]
    scores = []
    for competitor in selections:
        comp = comp_ref.child(competitor)
        comp_score = [comp.child("marks").get(), comp.child("score").get()]
        scores.append(comp_score)

    app.logger.info(f"score info: {selections}, {scores}")
    name = str(user["first_name"]+" "+user["last_name"])
    return render_template('profile.html', pfp=user["pfp"], name=name, selections=selections, scores=scores)

if __name__ == "__main__":
    app.run(debug=True)
