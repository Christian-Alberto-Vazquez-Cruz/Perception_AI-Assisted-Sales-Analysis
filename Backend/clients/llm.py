from groq import Groq


class LLMClient:
    def __init__(self, settings):
        self.configured = bool(settings.groq_api_key and settings.groq_api_key.get_secret_value().strip())
        self.model = settings.llm_model
        self.client = Groq(api_key=settings.groq_api_key.get_secret_value(), timeout=90, max_retries=0) if self.configured else None

    def _request(self, messages, stream=False):
        if not self.client:
            raise RuntimeError('Configura GROQ_API_KEY en Backend/.env.')
        return self.client.chat.completions.create(model=self.model, messages=messages, max_completion_tokens=3000, reasoning_effort='low', temperature=0.15, stream=stream)

    def complete(self, messages):
        result = self._request(messages)
        return result.choices[0].message.content or ''

    def stream(self, messages):
        chunks = self._request(messages, stream=True)
        try:
            for chunk in chunks:
                if chunk.choices and chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
        finally:
            close = getattr(chunks, 'close', None)
            if close:
                close()
