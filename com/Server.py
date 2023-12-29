import json
from flask import Flask, Response, request
from Configuration import Configuration
from Controller import Controller


class Server:
    JSON = 'application/json'
    def __init__(
            self,
            controller: Controller,
            configuration: Configuration,
            host = '0.0.0.0',
            port = 5000):
        self.controller = controller
        self.configuration = configuration
        self.app = Flask(__name__)
        self.host = host
        self.port = port

    def start(self):
        self.app.add_url_rule('/', view_func=self.ok)
        self.app.add_url_rule('/config', methods=['GET', 'POST'], view_func=self.config)
        self.app.add_url_rule('/times', methods=['GET', 'POST'], view_func=self.times)
        self.app.add_url_rule('/breakdown', methods=['GET'], view_func=self.breakdown)

        self.app.run(host=self.host, port=self.port)

    def ok(self):
        return Response("OK", mimetype='text/xml')

    def times(self):
        if request.method == 'GET':
            up_to_date_config_data = Configuration(self.configuration.file_path).data()
            config_json = json.dumps(up_to_date_config_data)
            return Response(config_json, mimetype=Server.JSON)
        else:
            content_type = request.headers['Content-Type']
            print(f"received content-type {content_type}")
            if (content_type == 'application/json'):
                up_to_date_config_data = Configuration(self.configuration.file_path).data()
                copy = dict(up_to_date_config_data)
                copy['water_change_times'] = request.get_json()
                self.configuration.write_data(copy)
                return Response(f"written times {copy} ok", mimetype='text/xml', status=201,)
            else:
                return Response(f"content-type not supported {content_type}", status=500,)

    def config(self):
        if request.method == 'GET':
            up_to_date_config_data = Configuration(self.configuration.file_path).data()
            config_json = json.dumps(up_to_date_config_data)
            return Response(config_json, mimetype=Server.JSON)
        else:
            content_type = request.headers['Content-Type']
            print(f"received content-type {content_type}")
            if (content_type == 'application/json'):
                to_write_data = request.get_json()
                self.configuration.write_data(to_write_data)
                return Response(f"written times {to_write_data} ok", mimetype='text/xml', status=201,)
            else:
                return Response(f"content-type not supported {content_type}", status=500,)

    def breakdown(self):
        return Response(json.dumps(self.controller.breakdown()), mimetype=Server.JSON)
