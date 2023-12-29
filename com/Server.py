import json
from flask import Flask
from Progress import ProgressTracker
from Controller import Controller


class Server:
    def __init__(
            self,
            progress_tracker: ProgressTracker,
            controller: Controller,
            host = '0.0.0.0',
            port = 5000):
        self.progress_tracker = progress_tracker,
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
        val = self.sump.temperature_breakdown()
        self.progress_tracker.write_ln(f"val is {val}")
        return json.dumps(val)
