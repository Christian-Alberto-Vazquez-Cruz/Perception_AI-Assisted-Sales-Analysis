from Backend.clients.llm import LLMClient
from Backend.core.config import Settings
from Backend.services.chat import provider_error_message


def main():
    config = Settings()
    client = LLMClient(config)
    if not client.configured:
        raise SystemExit('Configura GROQ_API_KEY en Backend/.env o en esta terminal.')
    prompt = [{'role': 'user', 'content': 'Responde exactamente OK.'}]
    try:
        answer = client.complete(prompt)
        streamed = ''.join(client.stream(prompt))
    except Exception as exc:
        raise SystemExit(provider_error_message(exc)) from None
    assert 'OK' in answer and 'OK' in streamed, 'No se recibió la respuesta esperada.'
    print('Groq directo correcto: respuesta completa y streaming con', config.llm_model)


if __name__ == '__main__':
    main()
