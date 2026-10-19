from Backend.core.config import Settings
from Backend.clients.embeddings import EmbeddingClient
from Backend.repositories.knowledge import ChromaRepository, KnowledgeFilesRepository
from Backend.services.knowledge import KnowledgeService


def main():
    config = Settings()
    service = KnowledgeService(KnowledgeFilesRepository(config.knowledge_path), ChromaRepository(), EmbeddingClient(config.embedding_model))
    service.rebuild()
    result = service.search('¿Por qué bajaron las botanas en marzo? Patrón: Botanas importe -18%, resto estable. Caída concentrada en una categoría.')
    assert result, 'Sin resultados relevantes'
    assert any('Caída concentrada' in source['title'] or 'categoría' in source['title'] for source in result)
    print('RAG real correcto:', [source['id'] for source in result])


if __name__ == '__main__':
    main()
