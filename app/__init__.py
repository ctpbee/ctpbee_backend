from flask import request
from app.create_app import init_app

app = init_app()


@app.before_request
def before_request_handle():
    if "static" in request.path:
        return "", 404
