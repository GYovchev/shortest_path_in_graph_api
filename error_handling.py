from flask import Blueprint, current_app

from distance_engine.exception import InvalidLinkWeight, NodeDoesntExist, NoPathExists


class UnprocessableEntityError(Exception):
    def __init__(self, description: str):
        super(UnprocessableEntityError, self).__init__(description)


error_handling_blueprint = Blueprint('error_handling', __name__)


@error_handling_blueprint.app_errorhandler(UnprocessableEntityError)
def handle_unprocessable_entity(e):
    current_app.logger.info("Couldn't process user's request - {}".format(str(e)))
    return str(e), 422


@error_handling_blueprint.app_errorhandler(InvalidLinkWeight)
def handle_invalid_link_weight(e):
    current_app.logger.info("Invalid link weight received - {}".format(str(e)))
    return {"errorCode": "invalidLinkWeight", "longDescription": str(e)}, 400


@error_handling_blueprint.app_errorhandler(NodeDoesntExist)
def handle_node_doesnt_exist(e):
    current_app.logger.info(str(e))
    return {"errorCode": "nodeDoesntExist", "longDescription": str(e)}, 400


@error_handling_blueprint.app_errorhandler(NoPathExists)
def handle_path_doesnt_exist(e):
    current_app.logger.info(str(e))
    return {"errorCode": "noPathExists", "longDescription": str(e)}, 404


@error_handling_blueprint.app_errorhandler(Exception)
def handle_path_doesnt_exist(e):
    current_app.logger.error(str(e), exc_info=True)
    return {"errorCode": "internalError", "longDescription": "Internal error"}, 500
