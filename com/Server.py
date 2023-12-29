from flask import Flask

from Controller import Controller


class Server:
    def __init__(
            self,
            controller: Controller):
        self.controller = controller
        self.app = Flask(__name__)

    def start():
        self.app.run(debug = True)

    @app.route('/times')
    def times():
        return self.controller.times()

    @app.route('/breakdown')
        def breakdown():
            return self.controller.times()
