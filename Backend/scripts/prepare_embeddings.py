import argparse
from sentence_transformers import SentenceTransformer
from Backend.core.config import Settings

SOURCE = 'sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2'


def main():
    parser = argparse.ArgumentParser(description='Prepara el modelo local de embeddings. Usa la caché existente; --download permite descargarlo.')
    parser.add_argument('--download', action='store_true')
    args = parser.parse_args()
    target = Settings().embedding_model.resolve()
    if (target / 'modules.json').exists():
        print('El modelo local ya está preparado:', target)
        return
    model = SentenceTransformer(SOURCE, local_files_only=not args.download, token=False)
    target.mkdir(parents=True, exist_ok=True)
    model.save(str(target))
    print('Modelo local preparado:', target)


if __name__ == '__main__':
    main()
