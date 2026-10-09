from flask import Flask, render_template, url_for
from authlib.integrations.flask_client import OAuth
import firebase_admin
import pyrebase
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

"""firebaseConfig = {
  "apiKey": "AIzaSyC400bVkh_c0gVf7DhBBNHpUOCdhBlalZ4",
  "authDomain": "calculus-world-cup-bb810.firebaseapp.com",
  "databaseURL": "https://calculus-world-cup-default-rtdb.europe-west1.firebasedatabase.app",
  "projectId": "calculus-world-cup-bb810",
  "storageBucket": "calculus-world-cup-bb810.firebasestorage.app",
  "messagingSenderId": "123071097251",
  "appId": "1:123071097251:web:51640c9ab25347fa925216",
  "measurementId": "G-VNHWWS02DJ"
}

firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()
auth = firebase.auth()"""

@app.route('/')
def home():
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
    uuid = user_info["sub"]
    user = auth.create_user_with_email
    data = {"name": "ntheesh"}
    #db.push(data)             temp

    try:
        pass
        #supa_resp = supabase.auth.sign_in_with_oauth({"provider": "google", "token":token})#email})
    except Exception as e:
        app.logger.error(f"Error with supabase: {str(e)}")
        return "Error with database", 500
        
    return render_template('main.html')#user_info# test code

if __name__ == "__main__":
    app.run(debug=True)
