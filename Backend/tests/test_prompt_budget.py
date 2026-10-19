import json
from types import SimpleNamespace
from Backend.repositories.dataset import DatasetRepository
from Backend.services.metrics import summarize
from Backend.services.chat import compact_metrics, provider_error_message
from Backend.core.config import BASE


def test_compact_summary_preserves_every_value_and_source_id():
    records = DatasetRepository(BASE.parent / 'examples' / 'ventas_realistas_2026.json').load()
    sources = summarize(records)['sources']
    compact = compact_metrics(sources)
    reconstructed = {}
    for group in compact:
        if 'campos' in group:
            for row in group['filas']:
                data = dict(zip(group['campos'], row))
                reconstructed[data.pop('id')] = data
        else:
            reconstructed[group['id']] = group['data']
    assert reconstructed == {source['id']: source['data'] for source in sources}
    assert len(json.dumps(compact, ensure_ascii=False)) < len(json.dumps(sources, ensure_ascii=False)) * 0.60


def test_rate_limit_diagnostics_do_not_echo_provider_message():
    error = RuntimeError('sensitive request')
    error.status_code = 429
    error.body = {'error': {'message': 'Request too large for organization private-id'}}
    assert 'Esperar no reduce' in provider_error_message(error)
    assert 'private-id' not in provider_error_message(error)
    error.body = {}
    error.response = SimpleNamespace(headers={'retry-after': '12.4'})
    assert '13 segundos' in provider_error_message(error)
    error.response.headers = {'retry-after': 'invalid'}
    assert 'Espera un momento' in provider_error_message(error)
