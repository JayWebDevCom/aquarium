from flask import Flask

from Controller import Controller


class Server:
    def __init__(
            self,
            controller: Controller,
            host = '0.0.0.0',
            port = 5000):
        self.controller = controller
        self.app = Flask(__name__)
        self.host = host
        self.port = port

    def start(self):
        self.app.add_url_rule('/', view_func=self.ok)
        self.app.add_url_rule('/times', view_func=self.times)
        self.app.add_url_rule('/breakdown', view_func=self.breakdown)

        self.app.run(host=self.host, port=self.port, debug = True)

    def ok(self):
        return "OK"

    def times(self):
        return self.controller.times()

    def breakdown(self):
        return self.controller.breakdown()
