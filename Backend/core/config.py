from pathlib import Path
from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE = Path(__file__).resolve().parents[1]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=BASE / '.env', extra='ignore', populate_by_name=True)
    groq_api_key: SecretStr | None = None
    llm_model: str = 'openai/gpt-oss-120b'
    embedding_model: Path = BASE / 'models' / 'multilingual-minilm'
    rag_enabled: bool = True
    data_path: Path = BASE / 'data' / 'dataset.json'
    knowledge_path: Path = BASE / 'knowledge'
    cors_origins: list[str] = ['http://localhost:5173', 'http://127.0.0.1:5173']
