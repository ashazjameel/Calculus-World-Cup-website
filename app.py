from flask import Flask, render_template, url_for
from authlib.integrations.flask_client import OAuth
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

#app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
#app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

#db = SQLAlchemy(app)

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
    username = user_info["email"]
    return user_info#"test"

if __name__ == "__main__":
    app.run(debug=True)
