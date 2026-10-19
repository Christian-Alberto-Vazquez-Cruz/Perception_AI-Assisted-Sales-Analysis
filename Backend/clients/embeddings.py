from threading import Lock
from pathlib import Path
from sentence_transformers import SentenceTransformer


class EmbeddingClient:
    def __init__(self, model):
        directory = Path(model).resolve()
        if not directory.is_dir():
            raise ValueError('Falta el modelo local de embeddings. Ejecuta python -m Backend.scripts.prepare_embeddings antes de iniciar el backend.')
        self.model = SentenceTransformer(str(directory), local_files_only=True, token=False)
        self.lock = Lock()

    def encode(self, texts):
        with self.lock:
            return self.model.encode(texts, normalize_embeddings=True, show_progress_bar=False).tolist()
