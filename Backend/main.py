from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from Backend.core.config import Settings
from Backend.repositories.dataset import DatasetRepository
from Backend.services.datasets import DatasetService
from Backend.services.chat import ChatService
from Backend.api.routes import router


def create_app(settings=None, llm=None, knowledge=None):
    settings = settings or Settings()

    @asynccontextmanager
    async def lifespan(app):
        app.state.datasets = DatasetService(DatasetRepository(settings.data_path))
        active_llm = llm
        if active_llm is None:
            from Backend.clients.llm import LLMClient
            active_llm = LLMClient(settings)
        active_knowledge = knowledge
        if active_knowledge is None and settings.rag_enabled:
            from Backend.clients.embeddings import EmbeddingClient
            from Backend.repositories.knowledge import KnowledgeFilesRepository, ChromaRepository
            from Backend.services.knowledge import KnowledgeService
            active_knowledge = KnowledgeService(KnowledgeFilesRepository(settings.knowledge_path), ChromaRepository(), EmbeddingClient(settings.embedding_model))
            active_knowledge.rebuild()
        app.state.chat = ChatService(app.state.datasets, active_llm, active_knowledge)
        yield

    app = FastAPI(title='Perception · Asistente de una tienda', lifespan=lifespan)
    @app.exception_handler(RequestValidationError)
    async def validation_error(request, exc):
        return JSONResponse(status_code=422, content={'detail': [{'loc': list(e['loc']), 'msg': e['msg'], 'type': e['type']} for e in exc.errors()]})

    app.add_middleware(CORSMiddleware, allow_origins=settings.cors_origins, allow_methods=['GET', 'POST'], allow_headers=['Content-Type'])
    app.include_router(router)
    return app


app = create_app()
