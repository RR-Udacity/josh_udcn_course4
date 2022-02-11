from flask import Flask
from flask_prometheus_metrics import register_metrics
from werkzeug.middleware.dispatcher import DispatcherMiddleware

app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello from Python!"

register_metrics(app, app_version="v0.0.1", app_config="dev")

# Plug metrics WSGI app to your main app with dispatcher
dispatcher = DispatcherMiddleware(app.wsgi_app, {"/metrics": make_wsgi_app()})

if __name__ == "__main__":
    app.run(host="0.0.0.0")
