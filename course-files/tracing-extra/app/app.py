
import os
import time
import requests

from flask import Flask, jsonify

import logging
from jaeger_client import Config
from flask_opentracing import FlaskTracing

app = Flask(__name__)

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
    )

    # this call also sets opentracing.tracer
    return config.initialize_tracer()


#starter code
tracer = init_tracer('test-service')

# config = Config(
#     config={
#         'sampler':
#         {'type': 'const',
#          'param': 1},
#                         'logging': True,
#                         'reporter_batch_size': 1,},
#                         service_name="service")
# jaeger_tracer = config.initialize_tracer()
# tracing = FlaskTracing(jaeger_tracer, True, app)


# not entirely sure but I believe there's a flask_opentracing.init_tracing() missing here
# redis_opentracing.init_tracing(tracer, trace_all_classes=False)

with tracer.start_span('first-span') as span:
    span.set_tag('first-tag', '100')


@app.route('/')
def hello_world():
    return 'Hello World!'



@app.route('/alpha')
def alpha():
    with tracer.start_span('alpha') as span:
        for i in range(100):
            # do_heavy_work() # removed the colon here since it caused a syntax error - not sure about its purpose?

            if i % 100 == 99:
                time.sleep(10)
    return 'This is the Alpha Endpoint!'

 
@app.route('/beta')
def beta():
    with tracer.start_span('beta') as span:
        r = requests.get("https://www.google.com/search?q=python")
        dict = {}
        for key, value in r.headers.items():
            print(key, ":", value)
            dict.update({key: value})
        return jsonify(dict)


if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))