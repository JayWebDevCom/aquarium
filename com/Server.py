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

    @self.app.route('/times')
    def times():
        return self.controller.times()

    @self.app.route('/breakdown')
    def breakdown():
        return self.controller.times()
