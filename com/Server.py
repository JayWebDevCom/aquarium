import json
from datetime import datetime
from http import HTTPStatus
from http.client import HTTPException
from typing import List

from flask import Flask, Response, request
from flask_httpauth import HTTPBasicAuth
from waitress import serve
from werkzeug.exceptions import HTTPException
from werkzeug.security import check_password_hash

from Configuration import Configuration
from Controller import Controller


class Server:
    JSON = 'application/json'
    TEXT = 'text/xml'
    configuration: Configuration
    auth = HTTPBasicAuth()

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
        self.app.add_url_rule('/drains', methods=['GET', 'PATCH'], view_func=self.drains)
        self.app.add_url_rule('/breakdown', methods=['GET'], view_func=self.breakdown)
        self.app.register_error_handler(HTTPException, self.handle_exception)
        Server.configuration = self.configuration
        return self.app

    @staticmethod
    @auth.login_required
    def ok():
        return Response("OK", mimetype=Server.TEXT)

    @auth.login_required
    def times(self):
        if request.method == 'GET':
            up_to_date_config_data = Configuration(self.configuration.file_path).data()
            wc_times_json = json.dumps(up_to_date_config_data['water_change_times'])
            return Server.response_of(wc_times_json, Server.JSON, HTTPStatus.OK)

        elif request.method == 'PATCH' and request.headers['Content-Type'] == Server.JSON:
            new_water_change_times = request.get_json()['water_change_times']
            if not isinstance(new_water_change_times, list) or not Server.are_valid_times(new_water_change_times):
                raise AquariumServerListError()
            up_to_date_config_data = Configuration(self.configuration.file_path).data()
            up_to_date_config_data['water_change_times'] = new_water_change_times
            self.configuration.write_data(up_to_date_config_data)
            response_json = json.dumps(up_to_date_config_data['water_change_times'])
            return Server.response_of(response_json, Server.JSON, HTTPStatus.OK)

        else:
            raise AquariumServerError()

    @auth.login_required
    def drains(self):
        if request.method == 'GET':
            up_to_date_config_data = Configuration(self.configuration.file_path).data()
            td_times_json = json.dumps(up_to_date_config_data['tank_drain_times'])
            return Server.response_of(td_times_json, Server.JSON, HTTPStatus.OK)

        elif request.method == 'PATCH' and request.headers['Content-Type'] == Server.JSON:
            new_tank_drain_times = request.get_json()['tank_drain_times']
            if not isinstance(new_tank_drain_times, list) or not Server.are_valid_times(new_tank_drain_times):
                raise AquariumServerListError()
            up_to_date_config_data = Configuration(self.configuration.file_path).data()
            up_to_date_config_data['tank_drain_times'] = new_tank_drain_times
            self.configuration.write_data(up_to_date_config_data)
            response_json = json.dumps(up_to_date_config_data['tank_drain_times'])
            return Server.response_of(response_json, Server.JSON, HTTPStatus.OK)

        else:
            raise AquariumServerError()

    @auth.login_required
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

    @auth.login_required()
    def breakdown(self):
        return Server.response_of(json.dumps(self.controller.temperature_breakdown()), Server.JSON, HTTPStatus.OK)

    @staticmethod
    @auth.verify_password
    def verify_password(username, password):
        for user in Server.configuration.get('users'):
            if user["username"] == username:
                return check_password_hash(user["password"], password)
        return False

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

    @staticmethod
    def are_valid_times(times_list: List[str]) -> bool:
        for time in times_list:
            try:
                datetime.strptime(time, '%H:%M')
            except ValueError:
                return False
        return True


class AquariumServerError(HTTPException):
    code = HTTPStatus.INTERNAL_SERVER_ERROR
    name = "AquariumServerError"
    description = "Bad PATCH, possible wrong Content-Type"


class AquariumServerListError(HTTPException):
    code = HTTPStatus.INTERNAL_SERVER_ERROR
    name = "AquariumServerListError"
    description = "Bad PATCH, possible incorrect data type provided - list[str] required"
