from flask import Blueprint, render_template

printer = Blueprint("printer", __name__, template_folder="../templates")

@printer.route("", methods=["GET"])
def main():
    return render_template("printer.html")
