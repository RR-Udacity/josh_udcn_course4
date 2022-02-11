from flask import Flask, render_template, request
import logging
from jaeger_client import Config
from jaeger_client.metrics.prometheus import PrometheusMetricsFactory
from prometheus_flask_exporter.multiprocess import GunicornInternalPrometheusMetrics
from flask_opentracing import FlaskTracing

app = Flask(__name__)
metrics = GunicornInternalPrometheusMetrics(app)
metrics.info('app_info', 'Frontend App', version='0.0.1')

def init_tracer(service):
    logging.getLogger('').handlers = []
    logging.basicConfig(format='%(message)s', level=logging.DEBUG)

    config = Config(
        config={
            'sampler': {
                'type': 'const',
                'param': 1,
            },
            'logging': True,
        },
        service_name=service,
        validate=True,
        metrics_factory=PrometheusMetricsFactory(service_name_label=service)
    )

    # this call also sets opentracing.tracer
    return config.initialize_tracer()


jaeger_tracer = init_tracer('nd064course4-backend-service')
# only trace requests explicitly annotated to be traced, this will prevent tracing "non-functional" requests
# such as prometheus /metrics
tracing = FlaskTracing(jaeger_tracer, False, app)

@app.route("/")
@tracing.trace()
def homepage():
    return render_template("main.html")

metrics.register_default(
    metrics.counter(
        'by_path_counter', 'Request count by request paths',
        labels={'path': lambda: request.path}
    )
)

if __name__ == "__main__":
    app.run()
