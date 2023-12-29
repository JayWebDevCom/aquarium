from flask import Flask

from Controller import Controller


class Server:
    def __init__(
            self,
            controller: Controller):
        self.controller = controller
        self.app = Flask(__name__)
        # routes
        self.app.route('/')(self.ok)
        self.app.times('/times')(self.times)
        self.app.breakdown('/breakdown')(self.breakdown)

    def start(self):
        app.run(debug = True)

    def ok():
        return "OK"

    def times(self):
        return self.controller.times()

    def breakdown(self):
        return self.controller.breakdown()
