import json

import pytest
import requests


# pytest test.py

class TestRegistration:

    # with open('flask_app/test_credentials.json', 'r') as file:
    #     testdata = json.load(file)
    # @pytest.fixture(autouse=True)
    def test_register(self):
        # file = TestCases.testdata[0]["testcase1"]
        url = 'http://127.0.0.1:5000/register'
        data = {'username': 'Aasdf', 'password': 'As123456', 'email': 'ramesh@gmail.com'}
        response = requests.post(url=url, data=data)

        assert response.status_code == 200

    def test_register1(self):
        url = 'http://127.0.0.1:5000/register'
        data = {'username': '', 'password': '', 'email': 'ramesh@gmail.com'}
        response = requests.post(url=url, data=data)
        assert response.status_code == 400

    def test_register2(self):
        url = 'http://127.0.0.1:5000/register'
        data = {'username': '', 'password': ''}
        response = requests.post(url=url, data=data)
        assert response.status_code == 400


# class TestLogin:
#     def test_login(self):
#         # file = TestCases.testdata[0]["testcase1"]
#         url = 'http://127.0.0.1:5000/login'
#         data = {'username': 'Aasdf', 'password': 'As123456',}
#         response = requests.post(url=url, data=data)
#
#         assert response.status_code == 200
#
# class TestForgot:
#     def test_forgot(self):
#         url = 'http://127.0.0.1:5000/forgot'
#         data = {'email': 'ramesh@gmail.com'}
#         response = requests.post(url=url, data=data)
#
#         assert response.status_code == 200