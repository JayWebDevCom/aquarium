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
        # routes
        self.app.route('/')(self.ok)
        self.app.route('/times')(self.times)
        self.app.route('/breakdown')(self.breakdown)

    def start(self):
        self.app.run(debug = True)

    def ok():
        return "OK"

    def times(self):
        return self.controller.times()

    def breakdown(self):
        return self.controller.breakdown()
