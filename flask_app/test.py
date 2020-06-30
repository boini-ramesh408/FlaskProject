import json

import pytest
import requests


# pytest test.py

class TestRegistration:

    # with open('flask_app/test_credentials.json', 'r') as file:
    #     testdata = json.load(file)
    # @pytest.fixture(autouse=True)
    def test_register_api_given_username_and_password_when_valid_returns_status_code_200(self):
        # file = TestCases.testdata[0]["testcase1"]
        url = 'http://127.0.0.1:5000/register'
        data = {'username': 'absdcfgg', 'password': 'As123456', 'confirm_password': 'As123456',
                'email': 'acsdfgg@gmail.com'}
        response = requests.post(url=url, data=data)

        assert response.status_code == 200

    def test_register_api_given_username_and_password_when_invalid_returns_status_code_400(self):
        url = 'http://127.0.0.1:5000/register'
        data = {'username': '', 'password': '', 'confirm_password': 'As123456', 'email': 'ramesh@gmail.com'}
        response = requests.post(url=url, data=data)
        assert response.status_code == 400

    def test_register_api_given_username_and_password_and_email_when_invalid_returns_status_code_400(self):
        url = 'http://127.0.0.1:5000/register'
        data = {'username': '', 'password': ''}
        response = requests.post(url=url, data=data)
        assert response.status_code == 400


class TestLogin:
    def test_login_api_given_username_and_password_when_valid_returns_status_code_200(self):
        # file = TestCases.testdata[0]["testcase1"]
        url = 'http://127.0.0.1:5000/login'
        data = {'email': 'ramesh008@gmail.com', 'password': 'As121212', }
        response = requests.post(url=url, data=data)

        assert response.status_code == 200

    def test_login_api_given_username_and_password_when_invalid_returns_status_code_400(self):
        # file = TestCases.testdata[0]["testcase1"]
        url = 'http://127.0.0.1:5000/login'
        data = {'email': 'Aasdfe', 'password': 'As123456s', }
        response = requests.post(url=url, data=data)

        assert response.status_code == 400


class TestForgot:

    def test_forgot_api_given_email_when_valid_returns_status_code_200(self):
        url = 'http://127.0.0.1:5000/forgot'
        data = {'email': 'ramesh@gmail.com'}
        response = requests.post(url=url, data=data)

        assert response.status_code == 200

    def test_forgot_api_given_email_when_invalid_returns_status_code_400(self):
        url = 'http://127.0.0.1:5000/forgot'
        data = {'email': '123@gmail.com'}
        response = requests.post(url=url, data=data)

        assert response.status_code == 400
