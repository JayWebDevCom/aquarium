import json

from flask import Flask, Response, request
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
        self.app.add_url_rule('/', view_func=Server.ok)
        self.app.add_url_rule('/config', methods=['GET', 'POST'], view_func=self.config)
        self.app.add_url_rule('/times', methods=['GET', 'POST'], view_func=self.times)
        self.app.add_url_rule('/breakdown', methods=['GET'], view_func=self.breakdown)

        self.app.run(host=self.host, port=self.port)

    @staticmethod
    def ok():
        return Response("OK", mimetype='text/xml')

    def times(self):
        if request.method == 'GET':
            up_to_date_config_data = Configuration(self.configuration.file_path).data()
            wc_times_json = json.dumps(up_to_date_config_data['water_change_times'])
            return Server.response_of(wc_times_json, Server.JSON, 200)

        elif request.method == 'POST' and request.headers['Content-Type'] == 'application/json':
            up_to_date_config_data = Configuration(self.configuration.file_path).data()
            up_to_date_config_data['water_change_times'] = request.get_json()['water_change_times']
            self.configuration.write_data(up_to_date_config_data)
            response_json = json.dumps(up_to_date_config_data['water_change_times'])
            return Server.response_of(response_json, Server.JSON, 201)

        else:
            return Server.response_of(f"request error for request: {request}", Server.TEXT, 500)

    def config(self):
        if request.method == 'GET':
            up_to_date_config_data = Configuration(self.configuration.file_path).data()
            config_json = json.dumps(up_to_date_config_data)
            return Server.response_of(config_json, Server.JSON, 200)

        elif request.method == 'POST' and request.headers['Content-Type'] == Server.JSON:
            data = request.get_json()
            self.configuration.write_data(data)
            return Server.response_of(json.dumps(data), mimetype=Server.JSON, status=201)

        else:
            return Server.response_of(f"request error for request: {request}", Server.TEXT, 500)

    def breakdown(self):
        return Server.response_of(json.dumps(self.controller.breakdown()), Server.JSON, 200)

    @staticmethod
    def response_of(message: str, mimetype: str, status: int):
        return Response(message, mimetype=mimetype, status=status)
