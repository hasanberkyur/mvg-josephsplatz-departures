from flask import Flask, jsonify, render_template
from mvg_client import get_departures


app = Flask(__name__)


@app.route("/")
def index():
    """
    Render the main website.
    """
    data = get_departures()
    return render_template("index.html", data=data)


@app.route("/api/departures")
def api_departures():
    """
    Return departure data as JSON.
    Useful later to auto-refresh with JavaScript.
    """
    data = get_departures()
    return jsonify(data)


if __name__ == "__main__":
    app.run(debug=True)