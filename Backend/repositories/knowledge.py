import re
import unicodedata
from threading import RLock


def slug(text):
    normalized = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode().lower()
    return re.sub(r'[^a-z0-9]+', '-', normalized).strip('-')


class KnowledgeFilesRepository:
    def __init__(self, directory):
        self.directory = directory

    def load(self):
        fragments = []
        for path in sorted(self.directory.glob('*.md')):
            text = path.read_text(encoding='utf-8')
            sections = re.split(r'^##\s+(.+?)\s*$', text, flags=re.MULTILINE)
            for index in range(1, len(sections), 2):
                title, content = sections[index], sections[index + 1].strip()
                if not content:
                    continue
                identifier = f'k-{slug(path.stem)}-{slug(title)}'
                if any(f['id'] == identifier for f in fragments):
                    raise ValueError(f'Sección duplicada: {identifier}')
                fragments.append({'id': identifier, 'title': title, 'kind': 'knowledge', 'document': path.name, 'content': content})
        return fragments


class ChromaRepository:
    def __init__(self):
        import chromadb
        self.client = chromadb.EphemeralClient()
        self.lock = RLock()
        self.collection = None

    def rebuild(self, fragments, embeddings):
        with self.lock:
            if any(c.name == 'knowledge' for c in self.client.list_collections()):
                self.client.delete_collection('knowledge')
            self.collection = self.client.create_collection('knowledge', embedding_function=None, metadata={'hnsw:space': 'cosine'})
            if fragments:
                self.collection.add(ids=[f['id'] for f in fragments], documents=[f['content'] for f in fragments], metadatas=[{'title': f['title'], 'document': f['document']} for f in fragments], embeddings=embeddings)

    def search(self, embedding, limit=3):
        with self.lock:
            if not self.collection or not self.collection.count():
                return []
            result = self.collection.query(query_embeddings=[embedding], n_results=min(limit, self.collection.count()), include=['documents', 'metadatas', 'distances'])
        return [{'id': identifier, 'kind': 'knowledge', **metadata, 'content': content, 'distance': float(distance)} for identifier, metadata, content, distance in zip(result['ids'][0], result['metadatas'][0], result['documents'][0], result['distances'][0])]
