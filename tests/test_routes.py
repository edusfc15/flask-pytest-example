from flask import Flask
import json

from flask_pytest_example.handlers.routes import configure_routes

TEST_URL = '/post/test'

def test_base_route():
    app = Flask(__name__)
    app.config['WTF_CSRF_ENABLED'] = False # Sensitive
    configure_routes(app)
    client = app.test_client()
    url = '/'

    response = client.get(url)
    assert response.get_data() == b'Hello, World!'
    assert response.status_code == 200


def test_post_route__success():
    app = Flask(__name__)
    app.config['WTF_CSRF_ENABLED'] = False # Sensitive
    configure_routes(app)
    client = app.test_client()
    url = TEST_URL

    mock_request_headers = {
        'authorization-sha256': '123'
    }

    mock_request_data = {
        'request_id': '123',
        'payload': {
            'py': 'pi',
            'java': 'script'
        }
    }

    response = client.post(url, data=json.dumps(mock_request_data), headers=mock_request_headers)
    assert response.status_code == 200


def test_post_route__failure__unauthorized():
    app = Flask(__name__)
    app.config['WTF_CSRF_ENABLED'] = False # Sensitive
    configure_routes(app)
    client = app.test_client()
    url = TEST_URL

    mock_request_headers = {}

    mock_request_data = {
        'request_id': '123',
        'payload': {
            'py': 'pi',
            'java': 'script'
        }
    }

    response = client.post(url, data=json.dumps(mock_request_data), headers=mock_request_headers)
    assert response.status_code == 401


def test_post_route__failure__bad_request():
    app = Flask(__name__)
    app.config['WTF_CSRF_ENABLED'] = False # Sensitive
    configure_routes(app)
    client = app.test_client()
    url = TEST_URL

    mock_request_headers = {
        'authorization-sha256': '123'
    }

    mock_request_data = {}

    response = client.post(url, data=json.dumps(mock_request_data), headers=mock_request_headers)
    assert response.status_code == 400
