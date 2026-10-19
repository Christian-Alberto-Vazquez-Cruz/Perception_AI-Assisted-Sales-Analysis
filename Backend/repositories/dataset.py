import json
import os
import tempfile
from pydantic import TypeAdapter
from Backend.schemas.models import DatasetInput


class DatasetRepository:
    def __init__(self, path):
        self.path = path

    def load(self):
        if not self.path.exists():
            return None
        return TypeAdapter(DatasetInput).validate_json(self.path.read_text(encoding='utf-8'))

    def save(self, records):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        fd, name = tempfile.mkstemp(dir=self.path.parent, suffix='.tmp')
        try:
            with os.fdopen(fd, 'w', encoding='utf-8') as file:
                json.dump([r.model_dump(mode='json') for r in records], file, ensure_ascii=False, allow_nan=False)
                file.flush()
                os.fsync(file.fileno())
            os.replace(name, self.path)
        finally:
            if os.path.exists(name):
                os.unlink(name)
