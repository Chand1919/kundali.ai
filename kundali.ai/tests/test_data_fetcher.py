# test_data_fetcher.py
from src.data_fetcher import DataFetcher

class DummyResponse:
    def __init__(self, status_code, json_data=None, text=""):
        self.status_code = status_code
        self._json = json_data
        self.text = text

    def json(self):
        return self._json

def test_fetch_project_data(monkeypatch):
    # Mock function to replace requests.get
    def mock_get(*args, **kwargs):
        return DummyResponse(200, {"project": "test"})
    
    # Patch requests.get in the module where it's used
    monkeypatch.setattr("src.data_fetcher.requests", "get", mock_get)

    df = DataFetcher()
    result = df.fetch_project_data("1")
    assert result["project"] == "test"
