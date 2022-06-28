from fast_api_project import __version__

#TODO: Look at bob's affirmations API for ideas for testing
# https://github.com/bbelderbos/affirmations-api/blob/main/tests/test_main.py
#TODO: Add testing of endpoints
# from fastapi.testclient import TestClient
# client = TestClient(app)
#@pytest.fixture(scope="session")

# def client():
#     return TestClient(app)
# def test_function(client)
def test_version():
    assert __version__ == '0.1.0'
