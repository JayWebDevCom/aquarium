import json
from flask import Flask, Response
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
        return Response(json.dumps(self.controller.times()), mimetype=Server.JSON)

    def config(self):
        return Response(json.dumps(self.configuration.data()), mimetype=Server.JSON)

    def breakdown(self):
        return Response(json.dumps(self.controller.breakdown()), mimetype=Server.JSON)
