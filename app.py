from fileinput import filename
from flask import Flask, render_template, send_from_directory
import helper
from datetime import datetime, timezone
import sys

DATETIME_FORMAT = "%d. %m. %Y %H:%M:%S"
app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 300


@app.context_processor
def context_processor():
    return dict(
        grillbot_online=helper.is_grillbot_online(),
        loaded_at=datetime.now().strftime(DATETIME_FORMAT),
    )


@app.route("/")
def homepage():
    return render_template(
        "index.html",
        home_page=True,
        last_modification=helper.get_modification_date(
            app.template_folder, "index.html", DATETIME_FORMAT
        ),
    )


@app.route("/docs/<path:filename>")
def docs_page(filename):
    path = f"docs/{filename}.html"
    return render_template(
        path,
        home_page=False,
        last_modification=helper.get_modification_date(
            app.template_folder, path, DATETIME_FORMAT
        ),
    )


if __name__ == "__main__":
    is_debug = len(sys.argv) > 1 and sys.argv[1] == "--debug"
    ip = "127.0.0.1" if is_debug else "0.0.0.0"
    app.run(host=ip, port=80, debug=is_debug)
