from types import SimpleNamespace
from unittest.mock import patch
from Backend.core.config import Settings
from Backend.clients.llm import LLMClient


def test_groq_direct_complete_and_stream():
    config = Settings(_env_file=None, groq_api_key='test-key-not-real')
    with patch('Backend.clients.llm.Groq') as factory:
        client = LLMClient(config)
        factory.assert_called_once_with(api_key='test-key-not-real', timeout=90, max_retries=0)
        messages = [{'role': 'user', 'content': 'total'}]
        completion = factory.return_value.chat.completions.create
        completion.return_value = SimpleNamespace(choices=[SimpleNamespace(message=SimpleNamespace(content='Respuesta', reasoning='Internal reasoning should never be shown'))])
        assert client.complete(messages) == 'Respuesta'
        completion.assert_called_with(model='openai/gpt-oss-120b', messages=messages, max_completion_tokens=3000, reasoning_effort='low', temperature=0.15, stream=False)
        completion.return_value = iter([SimpleNamespace(choices=[SimpleNamespace(delta=SimpleNamespace(content=None, reasoning='Private reasoning'))]), SimpleNamespace(choices=[SimpleNamespace(delta=SimpleNamespace(content='Hola'))]), SimpleNamespace(choices=[])])
        assert list(client.stream(messages)) == ['Hola']
        completion.assert_called_with(model='openai/gpt-oss-120b', messages=messages, max_completion_tokens=3000, reasoning_effort='low', temperature=0.15, stream=True)


def test_groq_settings_from_env_file(tmp_path):
    config_file = tmp_path / '.env'
    config_file.write_text('GROQ_API_KEY=test-key-not-real\nLLM_MODEL=openai/gpt-oss-120b\n', encoding='utf-8')
    config = Settings(_env_file=config_file)
    assert config.llm_model == 'openai/gpt-oss-120b'
    assert config.groq_api_key.get_secret_value() == 'test-key-not-real'


def test_missing_key_does_not_initialize_groq():
    with patch('Backend.clients.llm.Groq') as factory:
        client = LLMClient(Settings(_env_file=None, groq_api_key=None))
        assert not client.configured
        factory.assert_not_called()
