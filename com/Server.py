from flask import Flask

from Controller import Controller


app = Flask(__name__)

class Server:
    def __init__(
            self,
            controller: Controller):
        self.controller = controller

    def start(self):
        app.run(debug = True)

    @app.route('/')
    def ok():
        return "OK"

    @app.route('/times')
    def times(self):
        return self.controller.times()

    @app.route('/breakdown')
    def breakdown(self):
        return self.controller.breakdown()
