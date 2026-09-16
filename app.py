from flask import Flask

app = Flask(__name__)

#test programme

@app.route("/test")
def hellow_world():
  return "Hello World"

if __name__ == "__main__":
  app.run()
