from flask import Flask, request
from flask.logging import default_handler
from flask_log_request_id import RequestID

import logging

from distance_engine import DistanceEngine
from distance_engine.exception import *
from error_handling import *
from log_formatting import logging_formatter

distance_engine = DistanceEngine()

default_handler.setFormatter(logging_formatter)

app = Flask(__name__)
RequestID(app)

app.logger.setLevel(logging.INFO)
app.register_blueprint(error_handling_blueprint)

@app.route('/v1/graph', methods=['PUT'])
def put_graph():
    if not request.is_json:
        raise UnprocessableEntityError("Request body should be a json.")
    graph_data = request.json
    try:
        graph = distance_engine.set_graph_from_dict(graph_data)
    except BadGraphDictionaryData as err:
        raise UnprocessableEntityError(str(err))
    return {"result": graph.to_dictionary()}


@app.route('/v1/graph/distance/<node_a>/<node_b>', methods=['GET'])
def get_distance_between_nodes(node_a, node_b):
    return {"result": distance_engine.get_distance(node_a, node_b)}


if __name__ == '__main__':
    app.run(threaded=True, debug=False)
