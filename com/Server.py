import json
from http import HTTPStatus
from http.client import HTTPException

from flask import Flask, Response, request
from werkzeug.exceptions import HTTPException
from waitress import serve

from Configuration import Configuration
from Controller import Controller


class Server:
    JSON = 'application/json'
    TEXT = 'text/xml'

    def __init__(
            self,
            controller: Controller,
            configuration: Configuration,
            host='0.0.0.0',
            port=5000):
        self.controller = controller
        self.configuration = configuration
        self.app = Flask(__name__)
        self.host = host
        self.port = port

    def start(self):
        serve(self.create_app(), host=self.host, port=self.port)

    def create_app(self) -> object:
        self.app.add_url_rule('/', view_func=Server.ok)
        self.app.add_url_rule('/config', methods=['GET', 'PUT'], view_func=self.config)
        self.app.add_url_rule('/times', methods=['GET', 'PATCH'], view_func=self.times)
        self.app.add_url_rule('/breakdown', methods=['GET'], view_func=self.breakdown)
        self.app.register_error_handler(HTTPException, self.handle_exception)
        return self.app

    @staticmethod
    def ok():
        return Response("OK", mimetype=Server.TEXT)

    def times(self):
        if request.method == 'GET':
            up_to_date_config_data = Configuration(self.configuration.file_path).data()
            wc_times_json = json.dumps(up_to_date_config_data['water_change_times'])
            return Server.response_of(wc_times_json, Server.JSON, HTTPStatus.OK)

        elif request.method == 'PATCH' and request.headers['Content-Type'] == Server.JSON:
            new_water_change_times = request.get_json()['water_change_times']
            if not isinstance(new_water_change_times, list):
                raise AquariumServerListError()
            up_to_date_config_data = Configuration(self.configuration.file_path).data()
            up_to_date_config_data['water_change_times'] = new_water_change_times
            self.configuration.write_data(up_to_date_config_data)
            response_json = json.dumps(up_to_date_config_data['water_change_times'])
            return Server.response_of(response_json, Server.JSON, HTTPStatus.OK)

        else:
            raise AquariumServerError()

    def config(self):
        if request.method == 'GET':
            up_to_date_config_data = Configuration(self.configuration.file_path).data()
            config_json = json.dumps(up_to_date_config_data)
            return Server.response_of(config_json, Server.JSON, HTTPStatus.OK)

        elif request.method == 'PUT' and request.headers['Content-Type'] == Server.JSON:
            data = request.get_json()
            self.configuration.write_data(data)
            return Server.response_of(json.dumps(data), mimetype=Server.JSON, status=HTTPStatus.OK)

        else:
            raise AquariumServerError()

    def breakdown(self):
        return Server.response_of(json.dumps(self.controller.temperature_breakdown()), Server.JSON, HTTPStatus.OK)

    @staticmethod
    def response_of(message: str, mimetype: str, status: int):
        return Response(message, mimetype=mimetype, status=status)

    @staticmethod
    def handle_exception(e):
        response = e.get_response()
        response.data = json.dumps({
            "code": e.code,
            "name": e.name,
            "description": e.description,
        })
        response.content_type = "application/json"
        return response


class AquariumServerError(HTTPException):
    code = HTTPStatus.INTERNAL_SERVER_ERROR
    name = "AquariumServerError"
    description = "Bad PATCH, possible wrong Content-Type"


class AquariumServerListError(HTTPException):
    code = HTTPStatus.INTERNAL_SERVER_ERROR
    name = "AquariumServerListError"
    description = "Bad PATCH, possible incorrect data type provided - list required"
