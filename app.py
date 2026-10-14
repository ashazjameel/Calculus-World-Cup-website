from flask import Flask, render_template, url_for, session, redirect
from authlib.integrations.flask_client import OAuth
from firebase import firebase
import os

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

firebaseApp = firebase.FirebaseApplication("https://calculus-world-cup-bb810-default-rtdb.europe-west1.firebasedatabase.app/", None)

@app.route('/')
def unlogged():
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
           "last_name": lname,
           "uuid": uuid}
    return firebaseApp.get("/user","test")
    test_data = firebaseApp.post("/user", data)#             temp

    try:
        pass
    except Exception as e:
        app.logger.error(f"Error with database: {str(e)}")
        return "Error with database", 500
        
    return redirect(url_for("home"))
    
@app.route("/home")
def home():
    return render_template('main.html')    #user_info
    
if __name__ == "__main__":
    app.run(debug=True)
