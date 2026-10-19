from fastapi.testclient import TestClient
from Backend.main import create_app
from Backend.tests.test_phase1 import settings, sample


class FakeLLM:
    configured = True

    def complete(self, messages):
        self.messages = messages
        return 'Botanas cayó 18% en marzo. [Métrica](#m-comparacion-1-1)'


def test_chat_prompt_only_aggregates(tmp_path):
    llm = FakeLLM()
    with TestClient(create_app(settings(tmp_path), llm=llm)) as client:
        assert client.post('/chat', json={'question': 'ventas'}).status_code == 409
        client.post('/datasets', json=sample())
        result = client.post('/chat', json={'question': '¿Por qué bajaron en marzo?', 'stream': False})
        assert result.status_code == 200
        assert '#m-comparacion-1-1' in result.json()['answer']
        prompt = llm.messages[1]['content']
        assert 'variacion_importe_pct' in prompt
        assert 'dias_con_registros' in prompt
        assert '2026-02-01' in prompt
        assert '"fecha":"2026-02-01","categoria"' not in prompt
        assert len(result.json()['sources']) > 0


def test_missing_token_and_bad_citations(tmp_path):
    llm = FakeLLM()
    llm.configured = False
    with TestClient(create_app(settings(tmp_path), llm=llm)) as client:
        client.post('/datasets', json=sample())
        assert client.post('/chat', json={'question': 'total', 'stream': False}).status_code == 503
    llm.configured = True
    llm.complete = lambda _: 'Inventado [dato](#no-existe)'
    with TestClient(create_app(settings(tmp_path), llm=llm)) as client:
        result = client.post('/chat', json={'question': 'total', 'stream': False}).json()
        assert 'No puedo ofrecer' in result['answer']
