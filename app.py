from flask import Flask, render_template, url_for
from authlib.integrations.flask_client import OAuth
import firebase_admin
from firebase_admin import db, credentials
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
"""
firebaseConfig = {
  apiKey="AIzaSyBJ0fS9hKXYXSPpXU3uhOOmUsn-pHZEHM8",
  authDomain="calculus-world-cup.firebaseapp.com",
  databaseURL="https://calculus-world-cup-default-rtdb.europe-west1.firebasedatabase.app",
  projectId="calculus-world-cup",
  storageBucket="calculus-world-cup.firebasestorage.app",
  messagingSenderId="1095708660529",
  appId="1:1095708660529:web:c498bbc7993da2694e1610",
  measurementId="G-L83DKYLSNH"}"""

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

    try:
        pass
        #supa_resp = supabase.auth.sign_in_with_oauth({"provider": "google", "token":token})#email})
    except Exception as e:
        app.logger.error(f"Error with supabase: {str(e)}")
        return "Error with database", 500
        
    return user_info# test code

if __name__ == "__main__":
    app.run(debug=True)
