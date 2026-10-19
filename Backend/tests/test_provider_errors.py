from types import SimpleNamespace
import pytest
from fastapi.testclient import TestClient
from Backend.main import create_app
from Backend.tests.test_phase1 import settings, sample
from Backend.tests.test_phase2 import FakeLLM


@pytest.mark.parametrize('stream', [True, False])
def test_no_credit_message_without_sensitive_exception(tmp_path, stream):
    class NoCredits(FakeLLM):
        def complete(self, messages):
            error = RuntimeError('sensitive provider details')
            error.response = SimpleNamespace(status_code=402)
            raise error

        def stream(self, messages):
            self.complete(messages)
            yield ''

    with TestClient(create_app(settings(tmp_path), llm=NoCredits())) as client:
        client.post('/datasets', json=sample())
        response = client.post('/chat', json={'question': 'total', 'stream': stream})
        assert 'facturación' in response.text
        assert 'Groq' in response.text
        assert 'sensitive' not in response.text
        assert response.status_code == (200 if stream else 502)
