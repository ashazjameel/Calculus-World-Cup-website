from flask import Flask, render_template
from authlib.integrations.flask_client import OAuth
import os

app = Flask(__name__)
oauth = OAuth(app)
google = oauth.register(
    name="google",
    client_id=os.environ.get("CLIENT_ID"),
    client_secret=os.environ.get("CLIENT_SECRET"),
    server_metadata_uri="http://accounts.google.com/.well-known/openid-configuration",
    client_kwards = {"scope":"openid profile email"}
)

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
