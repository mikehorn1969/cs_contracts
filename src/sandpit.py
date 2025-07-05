from flask import Flask
from markupsafe import escape

app = Flask(__name__)

@app.route("/<name>")
def hello(name):
    return f"Hello, {escape(name)}! what were you trying to do?"

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

if __name__ == '__main__':
    app.run(debug=True)