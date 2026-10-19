class KnowledgeService:
    def __init__(self, files, vectors, embeddings):
        self.files, self.vectors, self.embeddings = files, vectors, embeddings

    def rebuild(self):
        fragments = self.files.load()
        if not fragments:
            raise ValueError('No hay secciones ## en la base de conocimiento.')
        texts = [f"{f['title']}\n{f['content']}" for f in fragments]
        self.vectors.rebuild(fragments, self.embeddings.encode(texts))

    def search(self, query):
        embedding = self.embeddings.encode([query])[0]
        return [fragment for fragment in self.vectors.search(embedding) if fragment['distance'] <= 0.8]
