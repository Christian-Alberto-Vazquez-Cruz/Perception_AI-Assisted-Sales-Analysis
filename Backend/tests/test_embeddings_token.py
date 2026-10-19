from unittest.mock import patch


def test_embedding_client_is_local_and_unauthenticated(tmp_path):
    with patch('Backend.clients.embeddings.SentenceTransformer') as model:
        from Backend.clients.embeddings import EmbeddingClient
        EmbeddingClient(tmp_path)
        model.assert_called_once_with(str(tmp_path.resolve()), local_files_only=True, token=False)
