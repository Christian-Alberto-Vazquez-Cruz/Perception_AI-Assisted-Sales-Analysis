from Backend.repositories.knowledge import KnowledgeFilesRepository
from Backend.services.knowledge import KnowledgeService
from Backend.services.chat import ChatService
from Backend.services.datasets import DatasetService
from Backend.repositories.dataset import DatasetRepository
from Backend.schemas.models import Sale
from Backend.tests.test_phase1 import sample
from Backend.tests.test_phase2 import FakeLLM


class FakeEmbeddings:
    def encode(self, texts):
        self.texts = texts
        return [[1.0, 0.0] for _ in texts]


class FakeVectors:
    def rebuild(self, fragments, embeddings):
        self.fragments, self.embeddings = fragments, embeddings

    def search(self, embedding):
        assert embedding == [1.0, 0.0]
        return [{**self.fragments[0], 'distance': 0.1}]


def test_chunks_embeddings_and_combined_query(tmp_path):
    (tmp_path / 'guia.md').write_text('# Guía\n## Caída\nHipótesis, no certeza.\n## Acciones\nVerificar stock.', encoding='utf-8')
    files = KnowledgeFilesRepository(tmp_path)
    embeddings, vectors = FakeEmbeddings(), FakeVectors()
    rag = KnowledgeService(files, vectors, embeddings)
    rag.rebuild()
    assert [f['id'] for f in vectors.fragments] == ['k-guia-caida', 'k-guia-acciones']
    assert len(vectors.embeddings) == 2
    datasets = DatasetService(DatasetRepository(tmp_path / 'dataset.json'))
    datasets.replace([Sale.model_validate(r) for r in sample()])
    chat = ChatService(datasets, FakeLLM(), rag)
    messages, sources = chat.prepare('¿Marzo?')
    assert '¿Marzo?' in embeddings.texts[0]
    assert '-18.0%' in embeddings.texts[0]
    assert 'Hipótesis, no certeza' in messages[1]['content']
    assert any(s['id'] == 'k-guia-caida' for s in sources)


def test_real_chroma_explicit_embeddings():
    from Backend.repositories.knowledge import ChromaRepository
    vectors = ChromaRepository()
    fragments = [{'id': 'k-a', 'title': 'A', 'document': 'a.md', 'content': 'caída'}, {'id': 'k-b', 'title': 'B', 'document': 'b.md', 'content': 'pico'}]
    vectors.rebuild(fragments, [[1.0, 0.0], [0.0, 1.0]])
    assert vectors.search([1.0, 0.0])[0]['id'] == 'k-a'
    vectors.rebuild(fragments[:1], [[1.0, 0.0]])
    assert len(vectors.search([1.0, 0.0])) == 1
