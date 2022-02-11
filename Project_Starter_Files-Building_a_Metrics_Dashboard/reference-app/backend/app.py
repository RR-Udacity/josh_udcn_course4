import logging

from flask import Flask, render_template, request, jsonify
from flask_pymongo import PyMongo
from jaeger_client import Config
from jaeger_client.metrics.prometheus import PrometheusMetricsFactory
from prometheus_flask_exporter.multiprocess import GunicornInternalPrometheusMetrics
from flask_opentracing import FlaskTracing


app = Flask(__name__)
metrics = GunicornInternalPrometheusMetrics(app)


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

app.config['MONGO_DBNAME'] = 'example-mongodb'
app.config['MONGO_URI'] = 'mongodb://example-mongodb-svc.default.svc.cluster.local:27017/example-mongodb'

mongo = PyMongo(app)


@app.route('/')
@tracing.trace()
def homepage():
    return "Hello World"


@app.route('/api')
@tracing.trace()
def my_api():
    answer = "something"
    return jsonify(repsonse=answer)


@app.route('/star', methods=['POST'])
@tracing.trace()
def add_star():
  star = mongo.db.stars
  name = request.json['name']
  distance = request.json['distance']
  star_id = star.insert({'name': name, 'distance': distance})
  new_star = star.find_one({'_id': star_id })
  output = {'name' : new_star['name'], 'distance' : new_star['distance']}
  return jsonify({'result' : output})


if __name__ == "__main__":
    app.run()