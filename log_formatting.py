import logging
from flask import has_request_context, request
from flask_log_request_id import current_request_id


class RequestFormatter(logging.Formatter):
    def format(self, record):
        if has_request_context():
            record.url = request.url
            record.request_id = current_request_id()
        else:
            record.url = ''
            record.request_id = ''

        return super().format(record)


logging_formatter = RequestFormatter(
    'time=(%(asctime)s)  level=(%(levelname)s) module=(%(module)s) request_id=(%(request_id)s): %(message)s'
)