from flask import Flask

app = Flask(__name__)

#test programme

@app.route("/")
def home():
  return "test"

@app.route("/test")
def test():
  return render_template("not_index.html")

if __name__ == "__main__":
  app.run(debug=True)
