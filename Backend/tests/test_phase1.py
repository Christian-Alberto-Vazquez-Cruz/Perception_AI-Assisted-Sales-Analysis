from fastapi.testclient import TestClient
from Backend.main import create_app
from Backend.core.config import Settings


def settings(tmp_path):
    return Settings(data_path=tmp_path / 'dataset.json', rag_enabled=False)


def sample():
    return [{'fecha': '2026-02-01', 'categoria': 'Botanas', 'unidades': 100, 'importe': 1000}, {'fecha': '2026-03-01', 'categoria': 'Botanas', 'unidades': 82, 'importe': 820}, {'fecha': '2026-02-01', 'categoria': 'Bebidas', 'unidades': 50, 'importe': 500}, {'fecha': '2026-03-01', 'categoria': 'Bebidas', 'unidades': 50, 'importe': 500}]


def test_upload_metrics_restart_replace(tmp_path):
    config = settings(tmp_path)
    with TestClient(create_app(config)) as client:
        assert client.get('/datasets/current').status_code == 409
        response = client.post('/datasets', json=sample())
        assert response.status_code == 200
        result = response.json()
        assert result['totals']['importe'] == 2820
        assert result['monthly'][1]['variacion_importe_pct'] == -12
        row = next(r for r in result['comparisons'] if r['mes'] == '2026-03' and r['categoria'] == 'Botanas')
        assert row['variacion_importe_pct'] == -18
        assert result['peaks'][0]['importe'] == 1500
    with TestClient(create_app(config)) as client:
        assert client.get('/datasets/current').json()['totals']['importe'] == 2820
        assert client.post('/datasets', content='[{"fecha":"2026-01-01","categoria":"A","unidades":1,"importe":NaN}]', headers={'Content-Type': 'application/json'}).status_code == 422
        assert client.post('/datasets', json=sample()[:1]).json()['totals']['importe'] == 1000
    with TestClient(create_app(config)) as client:
        assert client.get('/datasets/current').json()['totals']['importe'] == 1000


def test_invalid_preserves_dataset(tmp_path):
    with TestClient(create_app(settings(tmp_path))) as client:
        client.post('/datasets', json=sample())
        for payload in [[], [{**sample()[0], 'importe': -1}], [{**sample()[0], 'fecha': '2026-02-30'}], [{**sample()[0], 'unidades': True}], [{**sample()[0], 'categoria': ' '}], [{**sample()[0], 'importe': '12'}]]:
            assert client.post('/datasets', json=payload).status_code == 422
        assert client.get('/datasets/current').json()['totals']['importe'] == 2820


def test_missing_month_and_zero_base(tmp_path):
    rows = [{'fecha': '2026-01-01', 'categoria': 'A', 'unidades': 0, 'importe': 0}, {'fecha': '2026-02-01', 'categoria': 'A', 'unidades': 2, 'importe': 10}, {'fecha': '2026-04-01', 'categoria': 'B', 'unidades': 2, 'importe': 20}]
    with TestClient(create_app(settings(tmp_path))) as client:
        result = client.post('/datasets', json=rows).json()
        assert result['monthly'][1]['variacion_importe_pct'] is None
        assert result['monthly'][2]['comparado_con'] is None
        assert next(r for r in result['comparisons'] if r['mes'] == '2026-04' and r['categoria'] == 'A')['importe'] is None
