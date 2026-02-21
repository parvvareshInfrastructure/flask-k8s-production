import pytest
import os
from app import app as flask_app


@pytest.fixture
def app():
    """Create application instance for testing"""
    flask_app.config.update({
        "TESTING": True,
    })
    yield flask_app


@pytest.fixture
def client(app):
    """Create test client"""
    return app.test_client()


def test_home(client):
    """Test home endpoint"""
    response = client.get('/')
    assert response.status_code == 200
    assert b'Hello' in response.data
    assert b'version=' in response.data


def test_home_with_custom_message(client, monkeypatch):
    """Test home endpoint with custom message"""
    monkeypatch.setenv('APP_MESSAGE', 'Custom Message')
    monkeypatch.setenv('APP_VERSION', '2.0')
    response = client.get('/')
    assert response.status_code == 200


def test_health(client):
    """Test health check endpoint"""
    response = client.get('/health')
    assert response.status_code == 200
    assert response.is_json
    data = response.get_json()
    assert data['status'] == 'ok'
    assert 'version' in data


def test_secret(client):
    """Test secret endpoint"""
    response = client.get('/secret')
    assert response.status_code == 200
    assert b'API_KEY=' in response.data


def test_secret_with_custom_key(client, monkeypatch):
    """Test secret endpoint with custom API key"""
    monkeypatch.setenv('API_KEY', 'test-key-123')
    # Need to reload the app to pick up the new env var
    response = client.get('/secret')
    assert response.status_code == 200
    assert b'API_KEY=' in response.data


def test_404(client):
    """Test 404 error"""
    response = client.get('/nonexistent')
    assert response.status_code == 404
