from threading import RLock
from fastapi import HTTPException
from Backend.services.metrics import summarize


class DatasetService:
    def __init__(self, repository):
        self.repository = repository
        self.lock = RLock()
        records = repository.load()
        self.summary = summarize(records) if records else None

    def replace(self, records):
        try:
            summary = summarize(records)
        except ValueError as exc:
            raise HTTPException(422, str(exc)) from exc
        with self.lock:
            self.repository.save(records)
            self.summary = summary
        return summary

    def snapshot(self):
        with self.lock:
            if self.summary is None:
                raise HTTPException(409, 'Primero sube un JSON de ventas.')
            return self.summary
