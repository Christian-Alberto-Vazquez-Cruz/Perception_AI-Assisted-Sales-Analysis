import json
from fastapi.testclient import TestClient
from Backend.main import create_app
from Backend.tests.test_phase1 import settings, sample
from Backend.tests.test_phase2 import FakeLLM


class StreamingLLM(FakeLLM):
    def stream(self, messages):
        yield 'Botanas cayó '
        yield '18%. [Métrica](#m-comparacion-1-1)'


def parse(response):
    return [(frame.splitlines()[0][7:], json.loads(frame.splitlines()[1][6:])) for frame in response.text.strip().split('\n\n')]


def test_stream_events_match_complete_contract(tmp_path):
    with TestClient(create_app(settings(tmp_path), llm=StreamingLLM())) as client:
        client.post('/datasets', json=sample())
        response = client.post('/chat', json={'question': '¿Botanas en marzo?'})
        assert response.headers['content-type'].startswith('text/event-stream')
        events = parse(response)
        assert [name for name, _ in events] == ['sources', 'delta', 'delta', 'done']
        assert events[-1][1]['answer'] == ''.join(data['text'] for name, data in events if name == 'delta')
        assert any(s['id'] == 'm-comparacion-1-1' for s in events[0][1]['sources'])


def test_stream_failure_and_invalid_final_citation(tmp_path):
    llm = StreamingLLM()
    def broken(_):
        yield 'Texto incompleto'
        raise RuntimeError('secret provider error')
    llm.stream = broken
    with TestClient(create_app(settings(tmp_path), llm=llm)) as client:
        client.post('/datasets', json=sample())
        result = client.post('/chat', json={'question': 'total'})
        assert parse(result)[-1][0] == 'error'
        assert 'secret provider' not in result.text
        llm.stream = lambda _: iter(['Texto sin citas'])
        result = client.post('/chat', json={'question': 'total'})
        assert 'No puedo ofrecer' in parse(result)[-1][1]['answer']


def test_errors_before_stream_headers(tmp_path):
    llm = StreamingLLM()
    with TestClient(create_app(settings(tmp_path), llm=llm)) as client:
        assert client.post('/chat', json={'question': 'total'}).status_code == 409
        client.post('/datasets', json=sample())
        llm.configured = False
        assert client.post('/chat', json={'question': 'total'}).status_code == 503
