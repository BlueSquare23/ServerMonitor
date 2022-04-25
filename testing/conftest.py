import sys
import pytest
from pathlib import Path
from app import run_app

app_path = '../ServerMonitor/app'

sys.path.insert(0, app_path)

application = run_app()

@pytest.fixture
def app():
    yield application

@pytest.fixture
def client(app):
    return app.test_client()
