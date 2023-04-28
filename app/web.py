import flask

app = flask.Flask(__name__)


@app.route("/")
def index():
    return flask.jsonify({"status": "OK"})
