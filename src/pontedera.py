import logging
from flask import Flask, render_template, jsonify
from routes.cod import cod
from routes.printer import printer
from dotenv import load_dotenv


load_dotenv()

app = Flask(__name__)
app.register_blueprint(cod, url_prefix="/cod")
app.register_blueprint(printer, url_prefix="/printer")


@app.route("/", methods=["GET"])
def default():
    return render_template("index.html")


@app.errorhandler(Exception)
def handle_error(e: Exception):
    logging.error("Internal error", {"error", str(e)})
    return "UnexpectedError", 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
