from flask import Flask, render_template

app = Flask(__name__)

#test programme

@app.route("/")
def home():
  return render_template("index.html")

@app.route("/api/test")
def test():
  return render_template("index.html")

if __name__ == "__main__":
  app.run(debug=True)
