from flask import Flask, Response, render_template, redirect
import helper
from datetime import datetime
import sys
from src.service_provider import ServiceProvider
import logging

logging.basicConfig(level=logging.INFO)

DATETIME_FORMAT = "%d. %m. %Y %H:%M:%S"
app = Flask(__name__)
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 300


@app.context_processor
def context_processor():
    return dict(
        grillbot_online=helper.is_grillbot_online(),
        loaded_at=datetime.now().strftime(DATETIME_FORMAT),
    )


@app.after_request
def after_request(response: Response) -> Response:
    response.headers["X-Frame-Options"] = "SAMEORIGIN"
    response.headers["X-Xss-Protection"] = "1; mode=block"
    response.headers["X-Content-Type-Options"] = "nosniff"

    return response


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
    try:
        return render_template(
            path,
            home_page=False,
            last_modification=helper.get_modification_date(
                app.template_folder, path, DATETIME_FORMAT
            ),
            data=dict()
        )
    except FileNotFoundError:
        return (
            f"<h1>Template not found</h1><p>Missing template with name <code>{filename}</code>.</p>",
            404,
        )


@app.route("/services/<string:service>")
def services_page(service: str):
    data = ServiceProvider(service).get_data()
    if data is None:
        return redirect("/")

    return render_template(
        "docs/service.html",
        home_page=False,
        last_modification=helper.get_modification_date(
            app.template_folder, "docs/service.html", DATETIME_FORMAT
        ),
        data=data,
    )


if __name__ == "__main__":
    is_debug = len(sys.argv) > 1 and sys.argv[1] == "--debug"
    ip = "127.0.0.1" if is_debug else "0.0.0.0"
    app.run(host=ip, port=80, debug=is_debug)
