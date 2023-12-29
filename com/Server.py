from flask import Flask

from Controller import Controller


app = Flask(__name__)

class Server:
    def __init__(
            self,
            controller: Controller):
        self.controller = controller

    def start():
        app.run(debug = True)

    @app.route('/times')
    def times():
        return self.controller.times()

    @app.route('/breakdown')
    def breakdown():
        return self.controller.breakdown()
