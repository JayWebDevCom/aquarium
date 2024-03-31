import json
import os
import tempfile
from base64 import b64encode
from typing import Any, Union, IO, List
from unittest import TestCase
from unittest.mock import Mock, MagicMock

import yaml
from werkzeug.security import generate_password_hash

from Configuration import Configuration
from Controller import Controller
from Server import Server


class TestServer(TestCase):
    tempfile: Union[IO[bytes], IO[Any]]
    server_app: object
    configuration: Configuration
    password = 'test-password'
    configuration_data = {
        'update_times': [':00', ':15', ':30', ':45'],
        'water_change_times': ['1', '2', '3'],
        'tank_drain_times': ['4', '5', '6'],
        'overfill_allowance': 2.5,
        'inner': {'value': 'inner-value'},
        'empty': [],
        'users': [
            {
                'username': 'test-user',
                'password': generate_password_hash(password)
            }
        ]

    }
    credentials = b64encode(f"{configuration_data['users'][0]['username']}:{password}".encode('ascii')).decode()

    @classmethod
    def setUp(cls):
        TestServer.tempfile = tempfile.NamedTemporaryFile(delete=False)
        with open(TestServer.tempfile.name, 'w') as file:
            yaml.dump(TestServer.configuration_data, file)
        TestServer.configuration = Configuration(TestServer.tempfile.name)

        mock = MagicMock()
        controller = Controller(sump=mock, scripts=[], config=TestServer.configuration,
                                progress_tracker=mock, tank_drain_valve=mock)
        TestServer.server_app = Server(controller, TestServer.configuration).create_app()

    @classmethod
    def tearDownClass(cls):
        os.remove(TestServer.tempfile.name)

    def test_breakdown_page(self):
        mock_controller = MagicMock()
        breakdown_data = {
            "name_key": "name_value",
            "list": ["one", "two", "three"],
            "object": {
                "foo": "bar"
            }
        }
        mock_controller.temperature_breakdown = Mock(return_value=breakdown_data)
        server_app = Server(mock_controller, TestServer.configuration).create_app()

        with server_app.test_client() as test_client:
            response = test_client.get('/breakdown', headers={"Authorization": f"Basic {TestServer.credentials}"})
            self.assertEqual(200, response.status_code)
            self.assertEqual('application/json', response.content_type)
            self.assertEqual(bytes(json.dumps(breakdown_data), encoding='utf-8'), response.data)

    def test_home_page(self):
        with TestServer.server_app.test_client() as test_client:
            response = test_client.get('/', headers={"Authorization": f"Basic {TestServer.credentials}"})
            self.assertEqual('text/xml; charset=utf-8', response.content_type)
            self.assertEqual(200, response.status_code)
            self.assertEqual(bytes('OK', encoding='utf-8'), response.data)

    def test_times(self):
        with TestServer.server_app.test_client() as test_client:
            response = test_client.get('/times', headers={"Authorization": f"Basic {TestServer.credentials}"})
            self.assertEqual(200, response.status_code)
            self.assertEqual('application/json', response.content_type)
            current_water_change_times = TestServer.configuration.water_change_times()
            self.assertEqual(bytes(json.dumps(current_water_change_times), encoding='utf-8'), response.data)

    def test_times_patch(self):
        with TestServer.server_app.test_client() as test_client:
            data = {
                "val": "foo",
                "obj": {
                    "key": "val"
                },
                "water_change_times": ["06:01", "07:01", "08:46"]
            }
            response = test_client.patch('/times', json=data,
                                         headers={"Authorization": f"Basic {TestServer.credentials}"})

            # response is as expected
            self.assertEqual(200, response.status_code)
            self.assertEqual('application/json', response.content_type)
            self.assertEqual(bytes(json.dumps(data['water_change_times']), encoding='utf-8'), response.data)

            # patch data is written to configuration
            up_to_date_config = Configuration(file_path=TestServer.configuration.file_path).data()
            self.assertEqual(data['water_change_times'], up_to_date_config['water_change_times'])

    def test_drains(self):
        with TestServer.server_app.test_client() as test_client:
            response = test_client.get('/drains', headers={"Authorization": f"Basic {TestServer.credentials}"})
            self.assertEqual(200, response.status_code)
            self.assertEqual('application/json', response.content_type)
            current_water_change_times = TestServer.configuration.tank_drain_times()
            self.assertEqual(bytes(json.dumps(current_water_change_times), encoding='utf-8'), response.data)

    def test_drains_patch(self):
        with TestServer.server_app.test_client() as test_client:
            data = {
                "val": "foo",
                "obj": {
                    "key": "val"
                },
                "tank_drain_times": ["11:01", "13:01", "17:59"]
            }
            response = test_client.patch('/drains', json=data,
                                         headers={"Authorization": f"Basic {TestServer.credentials}"})

            # response is as expected
            self.assertEqual(200, response.status_code)
            self.assertEqual('application/json', response.content_type)
            self.assertEqual(bytes(json.dumps(data['tank_drain_times']), encoding='utf-8'), response.data)

            # patch data is written to configuration
            up_to_date_config = Configuration(file_path=TestServer.configuration.file_path).data()
            self.assertEqual(data['tank_drain_times'], up_to_date_config['tank_drain_times'])

    def test_config_get(self):
        with TestServer.server_app.test_client() as test_client:
            response = test_client.get('/config', headers={"Authorization": f"Basic {TestServer.credentials}"})
            self.assertEqual(200, response.status_code)
            self.assertEqual('application/json', response.content_type)
            self.assertEqual(bytes(json.dumps(TestServer.configuration.data()), encoding='utf-8'), response.data)

    def test_config_put(self):
        with TestServer.server_app.test_client() as test_client:
            data = {
                "list": [1, 2, 3],
                "obj": {
                    "key": "val"
                },
                "val": "foo"
            }
            response = test_client.put('/config', json=data,
                                       headers={"Authorization": f"Basic {TestServer.credentials}"})

            # response is as expected
            self.assertEqual(200, response.status_code)
            self.assertEqual('application/json', response.content_type)
            self.assertEqual(bytes(json.dumps(data), encoding='utf-8'), response.data)

            # put data is written to configuration
            up_to_date_config = Configuration(file_path=TestServer.configuration.file_path).data()
            self.assertEqual(data, up_to_date_config)

    def test_error_page(self):
        with TestServer.server_app.test_client() as test_client:
            initial_config_data = TestServer.configuration.data()
            response = test_client.get('/error', headers={"Authorization": f"Basic {TestServer.credentials}"})

            # response is as expected
            self.assertEqual(404, response.status_code)
            self.assertEqual('application/json', response.content_type)
            self.assertEqual(bytes(json.dumps({
                "code": 404,
                "name": "Not Found",
                "description": "The requested URL was not found on the server. "
                               "If you entered the URL manually please "
                               "check your spelling and try again.",
            }), encoding='utf-8'), response.data)

            # patch data is not written to configuration
            up_to_date_config = Configuration(file_path=TestServer.configuration.file_path).data()
            self.assertEqual(initial_config_data, up_to_date_config)

    def test_bad_put(self):
        with TestServer.server_app.test_client() as test_client:
            initial_config_data = TestServer.configuration.data()
            data = {"list": [1, 2, 3]}
            response = test_client.put('/config', data=data,
                                       headers={"Authorization": f"Basic {TestServer.credentials}"})

            # response is as expected
            self.assertEqual(500, response.status_code)
            self.assertEqual('application/json', response.headers["Content-Type"])
            self.assertEqual(bytes(json.dumps({
                "code": 500,
                "name": "AquariumServerError",
                "description": "Bad PATCH, possible wrong Content-Type",
            }), encoding='utf-8'), response.data)

            # patch data is not written to configuration
            up_to_date_config = Configuration(file_path=TestServer.configuration.file_path).data()
            self.assertEqual(initial_config_data, up_to_date_config)

    def test_bad_patch_times(self):
        with TestServer.server_app.test_client() as test_client:
            initial_config_data = TestServer.configuration.data()
            data = {"water_change_times": "not a list"}
            response = test_client.patch('/times', json=data,
                                         headers={"Authorization": f"Basic {TestServer.credentials}"})

            # response is as expected
            self.assertEqual(500, response.status_code)
            self.assertEqual('application/json', response.headers["Content-Type"])
            self.assertEqual(bytes(json.dumps({
                "code": 500,
                "name": "AquariumServerListError",
                "description": "Bad PATCH, possible incorrect data type provided - list[str] required"
            }), encoding='utf-8'), response.data)

            # patch data is not written to configuration
            up_to_date_config = Configuration(file_path=TestServer.configuration.file_path).data()
            self.assertEqual(initial_config_data, up_to_date_config)

    def test_non_deserializable_water_change_times(self):
        self.run_validate_test("times", "water_change_times", ["07:p31", "25:01"])

    def test_non_deserializable_tank_drain_times(self):
        self.run_validate_test("drains", "tank_drain_times", ["21:61", "07:-31"])

    def run_validate_test(self, path: str, key_name: str, values: List[str]):
        for test_time in values:
            with TestServer.server_app.test_client() as test_client:
                initial_config_data = TestServer.configuration.data()
                data = {key_name: ["18:31", test_time]}
                response = test_client.patch(f'/{path}', json=data,
                                             headers={"Authorization": f"Basic {TestServer.credentials}"})

                # response is as expected
                self.assertEqual(500, response.status_code)
                self.assertEqual('application/json', response.headers["Content-Type"])
                self.assertEqual(bytes(json.dumps({
                    "code": 500,
                    "name": "AquariumServerListError",
                    "description": "Bad PATCH, possible incorrect data type provided - list[str] required"
                }), encoding='utf-8'), response.data)

                # patch data is not written to configuration
                up_to_date_config = Configuration(file_path=TestServer.configuration.file_path).data()
                self.assertEqual(initial_config_data, up_to_date_config)
