from flask import Flask

from Controller import Controller


class Server:
    def __init__(controller: Controller)
        self.controller = controller
        app = Flask(__name)

    def start():
        app.run(debug = True)

    @app.route('/times')
    def times()
        return self.controller.times()

    @app.route('/breakdown')
        def breakdown()
            return self.controller.times()
