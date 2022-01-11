from flask import Flask, render_template
from routes.cod import cod
from routes.printer import printer


app = Flask(__name__)
app.register_blueprint(cod, url_prefix="/cod")
app.register_blueprint(printer, url_prefix="/printer")


@app.route("/", methods=["GET"])
def default():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
